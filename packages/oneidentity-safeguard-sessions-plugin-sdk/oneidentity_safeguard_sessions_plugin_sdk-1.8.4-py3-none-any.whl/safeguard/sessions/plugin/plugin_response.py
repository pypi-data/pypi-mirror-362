#
# Copyright 2025 One Identity LLC.
# ALL RIGHTS RESERVED.
#
"""
.. py:module:: safeguard.sessions.plugin.plugin_response
    :synopsis: Helpers for building plugin responses.
"""
import json


class DenyReasons():
    """
    New in version 1.6.0

    The :class:`DenyReasons` holds the human readable reasons shown to the end-user.
    each message is a property on the class.

    .. code-block:: python


        #!/usr/bin/env pluginwrapper3

        from safeguard.sessions.plugin import AAResponse, DenyReasons

        class Plugin:
            def authenticate(self, gateway_user):
                try:
                    response = call_external_api()
                    if response.success:
                        return AAResponse.accept()
                    else:
                        return AAResponse.deny(deny_reason=DenyReasons().authentication_failure)
                except HTTPError:
                        return AAResponse.deny(deny_reason=DenyReasons().communication_error)
                except TimeOutError:
                        return AAResponse.deny(deny_reason=DenyReasons().backend_service_error)
    """

    __authentication_failure = "Authentication failed"
    __communication_error = "Communication Error"
    __backend_service_error = "Backend service unreachable"

    @property
    def authentication_failure(self):
        """
        Message indicates an authentication failure
        Used in :class:`MFAClient <safeguard.sessions.plugins.mfa_client.MFAClient>`

        :return type: str
        """
        return self.__authentication_failure

    @property
    def communication_error(self):
        """
        Message indicates communation error while using 3rd party services
        Used in :class:`MFAClient <safeguard.sessions.plugins.mfa_client.MFAClient>`

        :return type: str
        """
        return self.__communication_error

    @property
    def backend_service_error(self):
        """
        Message indicates error in 3rd party service. Usually server or HTTP errors.
        Used in :class:`MFAClient <safeguard.sessions.plugins.mfa_client.MFAClient>`

        :return type: str
        """
        return self.__backend_service_error


class AAResponse(dict):
    """
    The :class:`AAResponse` class represents an AA plugin response and provides methods for creating and modifying such
    responses.

    .. code-block:: python

        #!/usr/bin/env pluginwrapper3

        from safeguard.sessions.plugin import AAResponse

        class Plugin:
            def authenticate(self, gateway_user):
                if is_on_whitelist(gateway_user):
                    return AAResponse.accept()
                elif is_on_blacklist(gateway_user):
                    return AAResponse.deny(deny_reason="User is black listed")
                else:
                    return AAResponse.need_info("Who are you?", 'username')
    """

    @classmethod
    def accept(cls, reason=None):
        """
        Create a new ACCEPT response.

        :param str reason: will be placed in the metadata as ``{"reason": reason}``
        :return type: :class:`AAResponse`
        """
        return cls(verdict="ACCEPT").with_additional_metadata({"reason": cls.__set_reason(reason)})

    @classmethod
    def deny(cls, reason=None, deny_reason=None):
        """
        Create a new DENY response.

        :param str reason: will be placed in the metadata as ``{"reason": reason}``

        New in version 1.6.0

        :param str deny_reason: will be shown to the end-user
        :return type: :class:`AAResponse`
        """
        return cls(verdict="DENY").with_additional_metadata({"reason": cls.__set_reason(reason)}).with_reason(cls.__set_reason(deny_reason))

    @classmethod
    def need_info(cls, question, key, disable_echo=False):
        """
        Create a new NEEDINFO response.

        :param str question: question (or prompt) to display for the user
        :param str key: identifier key for the response (this will key the response in ``key_value_pairs`` parameter)
        :param bool disable_echo: turn echo off for the user input (useful for e.g. password input); default: False
        :return type: :class:`AAResponse`
        """
        return cls(verdict="NEEDINFO", question=(key, question, disable_echo))

    def with_additional_metadata(self, additional_metadata):
        """
        Set the additional metadata field in the response. Overwrites previous reason given in :meth:`accept`,
        :meth:`deny`.

        :param additional_metadata: this value will be stored a JSON in the *Additional metadata* column of the meta
            database.
        :return type: :class:`AAResponse`
        """
        if additional_metadata is None:
            return self

        if not isinstance(additional_metadata, str):
            additional_metadata = json.dumps(additional_metadata)

        return self.__with(additional_metadata=additional_metadata)

    def with_cookie(self, cookie):
        """
        Extend the response with a cookie.

        :param dict cookie: this value will be passed to the next call of the plugin in the ``cookie`` parameter
        :return type: :class:`AAResponse`
        """
        return self.__with(cookie=cookie)

    def with_gateway_user(self, gateway_user, gateway_groups=()):
        """
        Extend the response with a gateway username and its groups.

        :param str gateway_user: this value will override the current gateway user
        :param seq gateway_groups: these will override the current gateway user's groups; default: empty
        :return type: :class:`AAResponse`
        """
        return self.__with(gateway_user=gateway_user, gateway_groups=tuple(gateway_groups))

    def with_session_cookie(self, session_cookie):
        """
        Extend the response with a session cookie.

        :param dict session_cookie: this value will be passed to other plugins' (e.g. credstore) calls in their
            ``session_cookie`` parameter
        :return type: :class:`AAResponse`
        """
        return self.__with(session_cookie=session_cookie)

    def with_reason(self, reason):
        """
        New in version 1.6.0

        Extend the response with a human readable reason.
        This message is shown to the end-user if the plugin denies the connection

        :param reason str: the message shown to the end-user
        :return type: :class:`AAResponse`
        """
        return self.__with(reason=reason)

    def __with(self, **kwargs):
        self.update(kwargs)
        return self

    @staticmethod
    def __set_reason(reason):
        return reason or "N/A"
