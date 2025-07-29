#
# Copyright 2025 One Identity LLC.
# ALL RIGHTS RESERVED.
#
"""
.. py:module:: safeguard.sessions.plugin.connection_info
    :synopsis: Read-only container for parameters passed to AAA plugins.
"""


class ConnectionInfo:
    """
    The :class:`ConnectionInfo` class gives easy access to the parameters passed to a plugin. It is meant to
    represent a read-only record of the SPS sessions being processed. It is also the means to pass many parameters
    between functions if needed. *Note: SPS does not always know or pass all parameters in all hooks, in which case
    the corresponding value shall be None*.
    """

    def __init__(self,
                 gateway_domain=None,
                 gateway_groups=None,
                 gateway_password=None,
                 gateway_username=None,
                 key_value_pairs=None,
                 client_ip=None,
                 client_hostname=None,
                 client_port=None,
                 connection_name=None,
                 protocol=None,
                 session_id=None,
                 server_domain=None,
                 server_ip=None,
                 server_hostname=None,
                 server_port=None,
                 server_username=None
                 ):
        self._gateway_domain = gateway_domain
        self._gateway_groups = gateway_groups
        self._gateway_password = gateway_password
        self._gateway_username = gateway_username
        self._key_value_pairs = key_value_pairs
        self._client_ip = client_ip
        self._client_hostname = client_hostname
        self._client_port = client_port
        self._connection_name = connection_name
        self._protocol = protocol
        self._session_id = session_id
        self._server_domain = server_domain
        self._server_ip = server_ip
        self._server_hostname = server_hostname
        self._server_port = server_port
        self._server_username = server_username

    @property
    def connection_name(self):
        """
        Name of the connection policy (<protocol> Control -> Connections).
        """
        return self._connection_name

    @property
    def client_ip(self):
        """
        A string containing the IP address of the client.
        """
        return self._client_ip

    @property
    def client_port(self):
        """
        The port number of the client. Only available for AA plugins.
        """
        return self._client_port

    @property
    def client_hostname(self):
        """
        A string containing the hostname of the client or None if the address cannot be resolved.

        *New in version 1.5.0.*
        """
        return self._client_hostname

    @property
    def gateway_domain(self):
        """
        The domain name of the gateway user if known. Only set for Credential Store plugins.

        *New in version 1.2.0.*
        """
        return self._gateway_domain

    @property
    def gateway_groups(self):
        """
        The gateway groups of the gateway user as calculated by SPS.
        """
        return self._gateway_groups

    @property
    def gateway_password(self):
        """
        The gateway password as used, detected by SPS. Only set for Credential Store plugins. It is possible to
        have an empty string here in case the gateway authentication does not reveal the password itself. Empty
        string is presented in case of terminal server gateway mode of RDP.

        *New in version 1.2.0.*
        """
        return self._gateway_password

    @property
    def gateway_user(self):
        """
        See :meth:`gateway_username`. For backwards compatibility.
        """
        return self._gateway_username

    @property
    def gateway_username(self):
        """
        Contains the gateway username of the client, if already available (for example, if the user performed inband
        gateway authentication), otherwise its value is None.
        """
        return self._gateway_username

    @property
    def key_value_pairs(self):
        """
        A dictionary containing plugin-specific information, for example, it may include the username. This dictionary
        also contains any key-value pairs that the user specified. In the plugin, such fields are already parsed into
        separate key-value pairs.
        """
        return self._key_value_pairs

    @property
    def protocol(self):
        """
        The protocol used in the connection, one of ssh, telnet, rdp.
        """
        return self._protocol

    @property
    def session_id(self):
        """
        The unique identifier of the session.
        """
        return self._session_id

    @property
    def server_domain(self):
        """
        The domain name of the target user if known.

        *New in version 1.5.0.*
        """
        return self._server_domain

    @property
    def target_domain(self):
        """
        See :meth:`server_domain`. For backwards compatibility.

        *Deprecated.*
        """
        return self.server_domain

    @property
    def server_ip(self):
        """
        A string containing the IP address of the target server.

        *New in version 1.5.0.*
        """
        return self._server_ip

    @property
    def target_ip(self):
        """
        See :meth:`target_host`. For backwards compatibility.

        *Deprecated.*
        """
        return self.target_host

    @property
    def target_host(self):
        """
        Equals to :meth:`server_hostname` if available otherwise :meth:`server_ip`. For backwards compatibility.

        *Deprecated.*
        """
        return self.server_hostname or self.server_ip

    @property
    def target_server(self):
        """
        See :meth:`target_host`. For backwards compatibility.

        *Deprecated.*
        """
        return self.target_host

    @property
    def server_port(self):
        """
        The port number on the target server.

        *New in version 1.5.0.*
        """
        return self._server_port

    @property
    def target_port(self):
        """
        See :meth:`server_port`. For backwards compatibility.

        *Deprecated.*
        """
        return self.server_port

    @property
    def server_hostname(self):
        """
        A string containing the hostname of the target server or None if the address cannot be resolved.

        *New in version 1.5.0.*
        """
        return self._server_hostname

    @property
    def server_username(self):
        """
        The user name SPS uses to authenticate on the target server.

        *New in version 1.5.0.*
        """
        return self._server_username

    @property
    def target_username(self):
        """
        See :meth:`server_username`. For backwards compatibility.

        *Deprecated.*
        """
        return self.server_username
