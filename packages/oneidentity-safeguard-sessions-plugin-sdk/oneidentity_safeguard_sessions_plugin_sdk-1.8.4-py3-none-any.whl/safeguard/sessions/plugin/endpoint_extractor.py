#
# Copyright 2025 One Identity LLC.
# ALL RIGHTS RESERVED.
#
"""
.. py:module:: safeguard.sessions.plugin.endpoint_extractor
    :synopsis: Service to send requests to an endpoint and extract data from the response.
"""

import json
from http.client import responses
from urllib.parse import urljoin

import requests

from safeguard.sessions.plugin.logging import get_logger
from safeguard.sessions.plugin import PluginSDKRuntimeError

logger = get_logger(__name__)


class EndpointException(PluginSDKRuntimeError):
    """
    The :class:`EndpointException` exception is raised when an endpoint responds with non-OK status code or the
    response does not contain the data queried by the user. It is a subclass of
    :class:`PluginSDKRuntimeError <safeguard.sessions.plugin.exceptions.PluginSDKRuntimeError>`.
    """

    pass


class EndpointExtractor:
    """
    The :class:`EndpointExtractor` class represents an utility class which sends GET and POST requests to an URL, then
    extracts data from the responses.

     .. py:attribute:: base_url

        The :py:attr:`self.base_url <base_url>` attribute contains the common prefix of the URLs to where the HTTP
        requests will be sent. If :py:attr:`self.base_url <base_url>` is not specified, then the user must provide the
        full URL when calling :py:meth:`extract_data_from_endpoint`.
    """

    def __init__(self, base_url=None):
        self.base_url = base_url

    def extract_data_from_endpoint(
        self, session, endpoint_url, data_path=None, method="get", headers=None, data=None, params=None,
    ):
        """
        The :meth:`extract_data_from_endpoint` method uses invoke_http_method to invokes a HTTP method on the
        specified endpoint, then extracts the needed data from the endpoint's response.

        :param session: the requests.Session or
            :class:`RequestsTLS <safeguard.sessions.plugin.requests_tls.RequestsTLS>` object on which
            the HTTP method is invoked
        :param str endpoint_url: the URL where the HTTP request will be sent. If :py:attr:`self.base_url <base_url>` is
            defined, then it will be prepended to this URL.
        :param str data_path: path to the data to be retrieved, delimited by dots (eg. "key.another_key.last_key")
        :param str method: HTTP method to invoke, one of GET or POST
        :param dict headers: dictionary of HTTP Headers to send with the request
        :param dict data: dictionary, list of tuples, bytes, or file-like object to send in the body of the request
        :param dict params: dictionary, list of tuples or bytes to send in the query string for the request
        :return: the extracted data from the decoded response JSON
        :raises: :class:`EndpointException <safeguard.sessions.plugin.endpoint_extractor.EndpointException>`
        """
        response = self.invoke_http_method(session, endpoint_url, method, headers, data, params)
        full_url = urljoin(self.base_url, endpoint_url)
        if response.ok:
            # not logging the response as it may contain sensitive data
            logger.debug(f"Got 200 OK response from endpoint: {full_url}")
            try:
                response_json = json.loads(response.text)
                return EndpointExtractor._follow_path(
                    response_json,
                    data_path.split(".")
                ) if data_path else response_json
            except (KeyError, TypeError):
                raise EndpointException(
                    f"Endpoint ({full_url}) response did not contain the information", dict(data_path=data_path),
                )
        else:
            raise EndpointException(
                "Endpoint responded with NOK",
                dict(
                    status_code=response.status_code,
                    status_text=responses.get(response.status_code, "UNKNOWN"),
                    endpoint_url=full_url,
                    raw_response=response.text,
                ),
            )

    def invoke_http_method(self, session, endpoint_url, method, headers=None, data=None, params=None):
        """
        The :meth:`invoke_http_method` method invokes a HTTP method on the specified endpoint.

        :param session: the requests.Session or
            :class:`RequestsTLS <safeguard.sessions.plugin.requests_tls.RequestsTLS>` object on which
            the HTTP method is invoked
        :param str endpoint_url: the URL where the HTTP request will be sent. If :py:attr:`self.base_url <base_url>` is
            defined, then it will be prepended to this URL.
        :param str method: HTTP method to invoke, one of GET or POST
        :param dict headers: dictionary of HTTP Headers to send with the request
        :param dict data: dictionary, list of tuples, bytes, or file-like object to send in the body of the request
        :param dict params: dictionary, list of tuples or bytes to send in the query string for the request
        :return: response JSON
        :raises: :class:`EndpointException <safeguard.sessions.plugin.endpoint_extractor.EndpointException>`
        """
        full_url = urljoin(self.base_url, endpoint_url)
        logger.debug(f'Sending http request to endpoint: url="{full_url}", method="{method}"')
        try:
            if method == "get":
                return session.get(full_url, headers=headers, params=params)
            return session.post(full_url, headers=headers, data=json.dumps(data) if data else None, params=params,)
        except requests.exceptions.ConnectionError as exc:
            raise EndpointException(f"Connection error: {exc}")

    @classmethod
    def _follow_path(cls, d, path):
        return d if not path else cls._follow_path(d[path[0]], path[1:])
