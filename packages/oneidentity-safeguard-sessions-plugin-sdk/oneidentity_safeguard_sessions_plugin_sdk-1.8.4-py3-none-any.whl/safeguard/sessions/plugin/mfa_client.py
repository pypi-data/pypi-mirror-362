#
# Copyright 2025 One Identity LLC.
# ALL RIGHTS RESERVED.
#
"""
.. py:module:: safeguard.sessions.plugin.mfa_client
    :synopsis: Simple multi factor authentication client

The :class:`MFAClient` class can be used to implement simple multi factor authentication (MFA) service clients. The
following example shows the outline of a plugin for an imaginary "Acme" MFA that provides its services over HTTP/REST.

.. code-block:: python

    #!/usr/bin/env pluginwrapper3

    import requests
    from safeguard.sessions.plugin import AAPlugin, AAResponse
    from safeguard.sessions.plugin.mfa_client import MFAClient

    class AcmePlugin(AAPlugin):
        def do_authenticate(self):
            # Glue code to instantiate and execute an MFAClient
            client = AcmeClient.from_config(self.plugin_configuration)
            return client.execute_authenticate(self.username, self.mfa_identity, self.mfa_password)


    class AcmeClient(MFAClient):
        def __init__(self, disable_echo, ignore_connection_error, server_url, token):
            super().__init__('ACME plugin', ignore_connection_error)
            self.disable_echo = disable_echo
            self.server_url = server_url
            self.token = token

        @classmethod
        def from_config(cls, plugin_configuration, section='acme')
            # It is good practice to handle the plugin configuration in its own method.
            # This method will return an instance of AcmeClient
            return cls(
                # In case the client needs to ask for further password(s), it should set disable_echo like AAPlugin
                plugin_configuration.getboolean('auth', 'disable_echo', default=False),
                plugin_configuration.getboolean(section, 'ignore_connection_error', default=False),
                plugin_configuration.get(section, 'server_url'),
                plugin_configuration.get(section, 'token'),

            )

        def push_authenticate(self, mfa_identity):
            # Use the requests module to implement the HTTP/REST communication
            # for push notification,
            # Should return True/False depending on the outcome.
            return False

        def otp_authenticate(self, mfa_identity, otp):
            # Use the requests module to implement the HTTP/REST communication
            # for one-time password authentication.
            # Should return True/False depending on the outcome.
            return False

This plugin will support the common AAPlugin configuration options (:ref:`aa-plugin-config-label`) as well as an [acme]
section:

.. code-block:: ini

    [acme]
    ; ignore_connection_error=<yes|no>
    ; server_url=<server-url>
    ; token=<$-or-token>

"""
from .plugin_response import AAResponse, DenyReasons
from .logging import get_logger

RESULT_STARTEGY = {True: AAResponse.accept, False: AAResponse.deny}


class MFAClient:
    """
    The :class:`MFAClient` is a base class for simple MFA client implementations.
    """

    def __init__(self, branded_name, ignore_connection_error=False):
        self._ignore_connection_error = ignore_connection_error
        self.branded_name = branded_name
        self.logger = get_logger(__name__)

    def push_authenticate(self, mfa_identity):
        """
        The :meth:`push_authenticate` should implement handling push notification. It may return True/False or an
        :class:`AAResponse <safeguard.sessions.plugin.plugin_response.AAResponse>`. In case of asking for further
        password(s), the ``disable_echo`` parameter of
        :meth:`AAResponse.need_info <safeguard.sessions.plugin.plugin_response.AAResponse.need_info>` should come from
        the "[auth] disable_echo" configuration parameter.

        :param str mfa_identity: username/identity to authenticate
        :return: whether the push notification was successful or not
        :rtype: bool or :meth:`AAResponse <safeguard.sessions.plugin.plugin_response.AAResponse>`
        """
        raise NotImplementedError

    def otp_authenticate(self, mfa_identity, otp):
        """
        The :meth:`otp_authenticate` should implement checking one-time password. It may return True/False or an
        :class:`AAResponse <safeguard.sessions.plugin.plugin_response.AAResponse>`. In case of asking for further
        password(s), the ``disable_echo`` parameter of
        :meth:`AAResponse.need_info <safeguard.sessions.plugin.plugin_response.AAResponse.need_info>` should come from
        the "[auth] disable_echo" configuration parameter.

        :param str mfa_identity: username/identity to authenticate
        :param str otp: the password to check
        :return: whether the authentication was successful or not
        :rtype: bool or :meth:`AAResponse <safeguard.sessions.plugin.plugin_response.AAResponse>`
        """
        raise NotImplementedError

    def execute_authenticate(self, username, mfa_identity, mfa_password=None):
        """
        The :meth:`execute_authenticate` should be called from
        :meth:`AAPlugin.do_authenticate <safeguard.sessions.plugin.aa_plugin.AAPlugin.do_authenticate>`
        to execute the authentication. This method will dispatch to :meth:`push_authenticate` or
        :meth:`otp_authenticate` and handle errors as well as create the verdict towards SPS.

        New in version 1.6.0

        The deny verdicts now contains human readable deny verdicts

        :param str username: gateway user
        :param str mfa_identity: the MFA identity to use
        :param str mfa_password: the MFA password to check, or a False value to indicate push notification
        :return: AA plugin verdict
        :rtype: dict
        """
        try:
            if mfa_password:
                self.logger.info("Authenticating user '%s' as '%s' with OTP", username, mfa_identity)
                return self._translate_result_to_response(self.otp_authenticate(mfa_identity, mfa_password))
            else:
                self.logger.info("Authenticating user '%s' as '%s' with PUSH", username, mfa_identity)
                return self._translate_result_to_response(self.push_authenticate(mfa_identity))
        except MFAAuthenticationFailure as e:
            self.logger.debug("Authentication failed. Reason: %s", str(e))
            return AAResponse.deny(reason=str(e), deny_reason=DenyReasons().authentication_failure)
        except MFACommunicationError as e:
            self.logger.error(
                "Communication error while communicating with the {} service, "
                "you might need to upgrade your plugin".format(self.branded_name)
            )
            return AAResponse.deny(reason=str(e), deny_reason=DenyReasons().communication_error)
        except MFAServiceUnreachable as e:
            if self._ignore_connection_error:
                self.logger.warning("{} can not be accessed, allowing connection without MFA".format(self.branded_name))
                return AAResponse.accept(reason="{} is not reachable, fallback enabled".format(self.branded_name))
            else:
                self.logger.error("Backend service {} unreachable, failing authentication".format(self.branded_name))
                return AAResponse.deny(reason=str(e), deny_reason=DenyReasons().backend_service_error)

    @staticmethod
    def _translate_result_to_response(result):
        if isinstance(result, bool):
            return RESULT_STARTEGY.get(result, AAResponse.deny)()
        return result


class MFAAuthenticationFailure(Exception):
    """
    The :class:`MFAAuthenticationFailure` exception should be used to propagate server side authentication failure.
    """

    pass


class MFACommunicationError(Exception):
    """
    The :class:`MFACommunicationError` exception should be used in MFA clients to indicate that there was an error
    in the communication with the MFA service. For example use this exception if there is a mismatch between client and
    server protocol version or capabilities.
    """

    pass


class MFAServiceUnreachable(Exception):
    """
    The :class:`MFAServiceUnreachable` exception should be used in MFA clients to indicate that the MFA service could
    not be reached due to network issues.
    """

    pass
