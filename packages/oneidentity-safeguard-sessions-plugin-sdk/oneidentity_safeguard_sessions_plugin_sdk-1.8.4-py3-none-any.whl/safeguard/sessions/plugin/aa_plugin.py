#
# Copyright 2025 One Identity LLC.
# ALL RIGHTS RESERVED.
#
"""
.. py:module:: safeguard.sessions.plugin.aa_plugin
    :synopsis: AA plugin base class

AAPlugin way of working
^^^^^^^^^^^^^^^^^^^^^^^

When SPS calls the AAPlugin, it does so by creating an AAPlugin (or more likely derived class) instance. The
initialization of the instance processes the given plugin configuration and sets the logging level appropriately.

On the new AAPlugin instance SPS will make a call to ``authenticate``, ``authorize`` or ``session_ended``. In all cases
AAPlugin first collects the input parameters in
:class:`self.connection <safeguard.sessions.plugin.connection_info.ConnectionInfo>` and sets up
:py:attr:`self.cookie <AAPlugin.cookie>` and :py:attr:`self.session_cookie <AAPlugin.session_cookie>` attributes.

In case of ``authenticate`` the prescribed steps in :meth:`AAPlugin._authentication_steps` are executed, including
the user defined :meth:`AAPlugin.do_authenticate` and if all was successful then the steps in
:meth:`AAPlugin._post_successful_authentication_steps` are also executed.
The later steps can ask further questions from the user and do other housekeeping tasks.

In case of ``authorize`` the prescribed steps in :meth:`AAPlugin._authorization_steps` are executed, where the last
step is a call to the user defined :meth:`AAPlugin.do_authorize`.

In case of ``session_ended`` the prescribed steps in :meth:`AAPlugin._session_ended_steps` are executed, where the last
step is a call to the user defined :meth:`AAPlugin.do_session_ended`.

If a step returns with a verdict such as accept, deny or need info, then AAPlugin will add values stored in
:py:attr:`self.cookie <AAPlugin.cookie>` and :py:attr:`self.session_cookie <AAPlugin.session_cookie>` to the verdict
and return the result to SPS.

If a step returns with None, then AAPlugin marks it as done, and does not call it again in case the plugin returns
need info and the plugin is invoked again with the same callback.

AAPlugin methods and attributes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

"""
from .authentication_cache import AuthenticationCache
from .connection_info import ConnectionInfo
from .connection_limiter import ConnectionLimiter
from .plugin_configuration import RequiredConfigurationSettingNotFound
from .plugin_response import AAResponse
from .plugin_base import lazy_property, cookie_property, session_cookie_property, PluginBase
from .user_list import UserList
from .ldap_server_group_list import LDAPServerGroupList
from .user_mapping import UserMappingExplicit, UserMappingLdapServer


class AAPlugin(PluginBase):
    """
    The :class:`AAPlugin` class implements the common functionality of AA plugins. The following methods and
    attributes are available outside the constructor - on top of the ones inherited from
    :class:`PluginBase <safeguard.sessions.plugin.plugin_base.PluginBase` class:

    .. py:attribute:: connection

        The :py:attr:`self.connection <safeguard.sessions.plugin.connection_info.ConnectionInfo>` provides a read-only
        view of the parameters passed to the currently executing plugin hook, e.g. :meth:`do_authenticate`.

    .. py:attribute:: cookie

        The :py:attr:`self.cookie <cookie>` attribute is a dict that retains its contents between invocations of
        :meth:`do_authenticate`, :meth:`do_authorize` and :meth:`do_session_ended`.
        This is the way to pass data between these functions.

        When the plugin returns the contents are automatically returned to SPS. Note that when
        :meth:`AAResponse.with_cookie <safeguard.sessions.plugin.plugin_response.AAResponse.with_cookie>` is used, it
        takes precedence and updates :py:attr:`self.cookie <cookie>` before returning to SPS.

    .. py:attribute:: session_cookie

        The :py:attr:`self.session_cookie <session_cookie>` is similar to :py:attr:`self.cookie <cookie>`, but it is
        also visible in other plugins in the same session. When the plugin returns the contents are automatically
        returned to SPS. Note that when :meth:`AAResponse.with_session_cookie \
        <safeguard.sessions.plugin.plugin_response.AAResponse.with_session_cookie>` is used, it takes precedence and
        updates :py:attr:`self.session_cookie <session_cookie>` before returning to SPS.

    .. py:attribute:: username

        The :py:attr:`self.username <username>` is a
        :meth:`@cookie_property <safeguard.sessions.plugin.plugin_base.cookie_property>` which is equal to the gateway
        username, or if not present, then the target username, or finally the ``username`` value in the
        ``key_value_pairs``. If none of these are present then the connection is automatically denied as we don't have
        a username to work with.

        The initial value of :py:attr:`self.username <username>` is calculated by :meth:`_extract_username`. As a
        cookie property, the value of :py:attr:`self.username <username>` is retained in subsequent invocations of the
        plugin.

    .. py:attribute:: mfa_identity

        The :py:attr:`self.mfa_identity` is a
        :meth:`@cookie_property <safeguard.sessions.plugin.plugin_base.cookie_property>` which is equal to
        :py:attr:`self.username <username>` after mapping and transformations to the multi factor authentication
        identity.

        As a cookie property, the value of :py:attr:`self.mfa_identity <mfa_identity>` is retained in subsequent
        invocations of the plugin.

    .. py:attribute:: mfa_password

        The :py:attr:`self.mfa_password` is read-only property that is implemented by :meth:`_extract_mfa_password`.

"""

    MFA_PASSWORD_QUESTION = "Press Enter for push notification or type one-time password:"
    INTERACTIVE_PROTOCOLS = "rdp,ssh,telnet"

    def __init__(self, configuration, defaults=None, logger=None):
        super().__init__(configuration, defaults, logger)

    def do_authenticate(self):
        """
        The :meth:`do_authenticate` method should verify that the given MFA identity (``self.mfa_identity``) matches the
        given MFA password (``self.mfa_password``). In case the password is an empty string, the check should do a
        challenge-response or push notification or some other check. For details consult the *Creating custom
        Authentication and Authorization plugins* technical document.

        :return: dict with at least the key 'verdict' to indicate 'ACCEPT', 'DENY' or 'NEEDINFO'
        """

        return AAResponse.accept("Authentication hook not implemented")

    def do_authorize(self):
        """
        The :meth:`do_authorize` method should verify that the given MFA identity (``self.mfa_identity``)
        has authority (has the right) to access the given target asset (``self.connection.server_username``,
        ``self.connection.server_ip``, etc). For details consult the *Creating custom Authentication and
        Authorization plugins* technical document.

        :return: dict with at least the key 'verdict' to indicate 'ACCEPT', 'DENY'.
        """

        return AAResponse.accept("Authorize hook not implemented")

    def do_session_ended(self):
        """
        The :meth:`do_session_ended` hook can be used to send a log message related to the entire session or close the
        ticket related to the session if the plugin interacts with a ticketing system. For details consult the
        *Creating custom Authentication and Authorization plugins* technical document.

        :return: None
        """

        pass

    def _authentication_steps(self):
        """
        The :meth:`_authentication_steps` function returns a list of other functions to be called to execute the
        authentication task. The default implementation is as follows:

        .. literalinclude:: ../../../../src/safeguard/sessions/plugin/aa_plugin.py
            :pyobject: AAPlugin._authentication_steps
        """

        yield self._check_username
        yield self._check_user_list_whitelist
        yield self._check_ldap_group_whitelist
        yield self._check_authentication_cache
        yield self._map_username_explicit
        yield self._map_username_ldap
        yield self._transform_username
        yield self._ask_mfa_password
        yield self._log_authenticate_calculated_mfa_identity
        yield self.do_authenticate

    def _post_successful_authentication_steps(self):
        """
        The :meth:`_post_successful_authentication_steps` function returns a list of other functions to call be called
        after :meth:`_authentication_steps` in case of successful authentication. The functions listed here may only
        return ``None`` or a
        :meth:`AAResponse.need_info <safeguard.sessions.plugin.plugin_response.AAResponse.need_info>` reply.
        The default implementation is as follows:

        .. literalinclude:: ../../../../src/safeguard/sessions/plugin/aa_plugin.py
            :pyobject: AAPlugin._post_successful_authentication_steps
        """

        yield self._refresh_authentication_cache
        yield self._ask_questions

    def _authorization_steps(self):
        """
        The :meth:`_authorization_steps` function returns a list of other functions to call to finish the authentication
        task. The default implementation is as follows:

        .. literalinclude:: ../../../../src/safeguard/sessions/plugin/aa_plugin.py
            :pyobject: AAPlugin._authorization_steps
        """

        yield self._log_authorize_calculated_mfa_identity
        yield self._check_and_increase_client_connection_count
        yield self.do_authorize

    def _session_ended_steps(self):
        """
        The :meth:`_session_ended_steps` function returns a list of other functions to call to finish the session_ended
        task. The functions in the list must return with None. The default implementation is as follows:

        .. literalinclude:: ../../../../src/safeguard/sessions/plugin/aa_plugin.py
            :pyobject: AAPlugin._session_ended_steps
        """

        yield self._decrease_client_connection_count
        yield self.do_session_ended

    def _extract_username(self):
        """
        The :meth:`_extract_username` method may be overridden to modify the calculation of the gateway username. For
        example to introduce a new key_value_pair that can be the source of the username.

        If this method returns None, then AAPlugin automatically denies the connection.

        :return: str or None
        """

        gw_username = (
            self.connection.gateway_user or self.connection.key_value_pairs.get("gu")
        )

        return (
            gw_username
            or self.remove_upn_suffix(self.connection.server_username)
            or self.remove_upn_suffix(self.connection.key_value_pairs.get("username"))
        )

    def remove_upn_suffix(self, username):
        if (
            username
            and self.plugin_configuration.get(
                "ignore_upn_suffix_for_rdp", "ignore", default="true"
            )
            == "true"
            and self.connection.protocol.lower() in ("rdp", "tsg")
            and "@" in username
        ):
            return username.rsplit("@", 1)[0]

        return username

    def _map_username_explicit(self):
        """
        The :meth:`_map_username_explicit` method is implementing the ``[usermapping source=explicit]`` section in the
        configuration. It may alter the value of :py:attr:`self.mfa_identity <mfa_identity>`.
        """

        self.mfa_identity = (
            UserMappingExplicit.map_username(
                self.mfa_identity, self.plugin_configuration, section="usermapping source=explicit"
            )
            or self.mfa_identity
        )

    def _map_username_ldap(self):
        """
        The :meth:`_map_username_ldap` method is implementing the ``[usermapping source=ldap_server]`` section in the
        configuration. It may alter the value of :py:attr:`self.mfa_identity <mfa_identity>`.
        """

        if self._ldap_user_mapping:
            self.mfa_identity = self._ldap_user_mapping.map_username(self.mfa_identity) or self.mfa_identity

    def _transform_username(self):
        """
        The :meth:`_transform_username` method is implementing the ``[username_transform]`` section in the
        configuration. It may alter the value of :py:attr:`self.mfa_identity <mfa_identity>`.
        """

        domain_to_append = self.plugin_configuration.get("username_transform", "append_domain")
        if domain_to_append and "@" not in self.mfa_identity:
            self.mfa_identity = self.mfa_identity + "@" + domain_to_append

    @cookie_property
    def mfa_identity(self):
        return self.username

    @cookie_property
    def username(self):
        return self._extract_username()

    def _check_username(self):
        """
        The :meth:`_check_username` method checks that the plugin received a user identity to work with. It should
        return :meth:`AAResponse.deny <safeguard.sessions.plugin.plugin_response.AAResponse.deny>` verdict if there
        is no username, otherwise None.
        """

        if not self.username:
            self.logger.error("No username identified")
            return AAResponse.deny("No username identified")

    @lazy_property
    def _ldap_user_mapping(self):
        try:
            return UserMappingLdapServer.from_config(
                self.plugin_configuration, section="usermapping source=ldap_server"
            )
        except RequiredConfigurationSettingNotFound:
            return None

    @lazy_property
    def _user_whitelist(self):
        try:
            return UserList.from_config(self.plugin_configuration, section="whitelist source=user_list")
        except RequiredConfigurationSettingNotFound:
            return None

    @lazy_property
    def _ldap_group_whitelist(self):
        try:
            return LDAPServerGroupList.from_config(
                self.plugin_configuration, section="whitelist source=ldap_server_group"
            )
        except RequiredConfigurationSettingNotFound:
            return None

    def _check_user_list_whitelist(self):
        if self._user_whitelist and self.username in self._user_whitelist:
            self.logger.info("User {} whitelisted based on user list".format(self.username))
            return AAResponse.accept("User whitelisted based on user list")

    def _check_ldap_group_whitelist(self):
        if self._ldap_group_whitelist and self.username in self._ldap_group_whitelist:
            self.logger.info("User {} whitelisted based on ldap group".format(self.username))
            return AAResponse.accept("User whitelisted based on ldap group")

    def _check_authentication_cache(self):
        if self._authentication_cache.try_authenticate():
            self.logger.info("User {} allowed based on cached authentication".format(self.username))
            self._set_private("authenticated_from_cache", True)
            return AAResponse.accept("User allowed based on cached authentication")

    def _refresh_authentication_cache(self):
        if self._get_private("authenticated_from_cache"):
            self.logger.info("No cache update as previous authentication happened from authetication cache")
            return
        self.logger.info("Updating authentication cache")
        self._authentication_cache.cache_authentication()

    @lazy_property
    def _authentication_cache(self):
        return AuthenticationCache.from_config(self.plugin_configuration, self.connection.client_ip, self.username)

    def _check_and_increase_client_connection_count(self):
        keys = (self.connection.client_ip, self.username)
        connection_limiter = self._create_client_connection_limiter(keys)
        if not connection_limiter.active():
            return
        self._set_private("client_conn_limit_keys", keys)
        if not connection_limiter.try_connect(self.connection.session_id):
            self.logger.info("User {} rejected due to connection limit reached".format(self.username))
            return AAResponse.deny("Connection limit reached")

    def _decrease_client_connection_count(self):
        keys = self._get_private("client_conn_limit_keys")
        if keys is None:
            return
        connection_limiter = self._create_client_connection_limiter(keys)
        connection_limiter.disconnect(self.connection.session_id)

    def _create_client_connection_limiter(self, keys):
        return ConnectionLimiter.from_config(
            plugin_config=self.plugin_configuration,
            keys=keys,
            section="connection_limit by=client_ip_gateway_user",
            limit_description="client ip and gateway user name",
        )

    @property
    def mfa_password(self):
        return self._extract_mfa_password()

    def _ask_mfa_password(self):
        if self._extract_mfa_password() is not None:
            return None

        question = self.plugin_configuration.get("auth", "prompt", default=self.MFA_PASSWORD_QUESTION)
        disable_echo = self.plugin_configuration.getboolean("auth", "disable_echo", default=False)
        return AAResponse.need_info(question + " ", "otp", disable_echo)

    def _extract_mfa_password(self):
        """
        The :meth:`_extract_mfa_password` method returns the value of ``self.connection.key_value_pairs['otp']``. The
        value is either specified as part of the username or if not, then AAPlugin will ask the user for it
        interactively on interactive protocols such as SSH. On non-interactive protocols like MS SQL the code will
        assume push notification and return the empty string.

        The :meth:`_extract_mfa_password` method may be overwritten to modify the calculation of the MFA password. For
        example to introduce a new key_value_pair that can be the source of the password.

        If this method returns None, then AAPlugin automatically asks for the password.

        :return: str or None
        """

        otp = self.connection.key_value_pairs.get("otp")
        if otp is not None:
            return otp

        interactive_protocols = [
            item.strip().lower() for item in self.plugin_configuration.get(
                "auth",
                "interactive_protocols",
                default=self.INTERACTIVE_PROTOCOLS
            ).split(",")
        ]
        if self.connection.protocol.lower() not in interactive_protocols:
            return ""
        else:
            return None

    def _log_authenticate_calculated_mfa_identity(self):
        self.logger.info("Authenticating user {} with MFA identity of {}".format(self.username, self.mfa_identity))

    def _log_authorize_calculated_mfa_identity(self):
        self.logger.info("Authorizing user {} with MFA identity of {}".format(self.username, self.mfa_identity))

    def authenticate(
        self,
        cookie,
        session_cookie,
        session_id,
        protocol,
        connection_name,
        client_ip,
        client_port,
        client_hostname,
        gateway_user,
        gateway_domain,
        server_username,
        server_domain,
        key_value_pairs
    ):
        """
        **Should not be modified.**

        The :meth:`authenticate` function is called by SPS directly. Should not be modified, see
        :meth:`do_authenticate` for customization.
        """

        self._setup_self(
            cookie,
            session_cookie,
            ConnectionInfo(
                session_id=session_id,
                protocol=protocol,
                connection_name=connection_name,
                client_ip=client_ip,
                client_port=client_port,
                client_hostname=client_hostname,
                gateway_username=gateway_user,
                gateway_domain=gateway_domain,
                server_username=server_username,
                server_domain=server_domain,
                key_value_pairs=key_value_pairs
            )
        )
        return self.finalize_hook(self._add_cookies(self._add_gateway_user(self._execute_authenticate())))

    def _execute_authenticate(self):
        if not self._get_private("successful_authentication"):
            auth_verdict = self._execute_steps(
                checkpoints_key="authenticate_checkpoints", steps=self._authentication_steps()
            )

            if auth_verdict is None:
                return AAResponse.deny("Unexpected error occured, authentication steps yield None")
            elif self._is_accept_verdict(auth_verdict):
                self._set_private("successful_authentication", True)
                self._set_private("saved_verdict", auth_verdict)
                return self._execute_post_success_authenticate()
            else:
                return auth_verdict
        else:
            return self._execute_post_success_authenticate()

    def _execute_post_success_authenticate(self):
        verdict = self._execute_steps(
            checkpoints_key="post_successful_authenticate_checkpoints",
            steps=self._post_successful_authentication_steps(),
        )

        if verdict is None:
            # Previous verdict is popped, because in case verdict is kept in the cookie,
            # than setting the cookie in the verdict creates a circular reference.
            return self._pop_private("saved_verdict")
        else:
            return verdict

    def _ask_questions(self):
        while True:
            number = self._get_private("question_sequence_number", 0) + 1
            question = self._get_question(number)
            if question:
                (prompt, key, disable_echo) = question
                if key in self.questions:
                    # already stored the answer
                    self._set_private("question_sequence_number", number)
                elif key in self.connection.key_value_pairs:
                    # already received an answer
                    self.questions[key] = self.connection.key_value_pairs[key]
                    self._set_private("question_sequence_number", number)
                else:
                    return AAResponse.need_info(*question)
            else:
                return None

    def _get_question(self, number):
        try:
            return (
                self.plugin_configuration.get("question_{}".format(number), "prompt", required=True) + " ",
                self.plugin_configuration.get("question_{}".format(number), "key", required=True),
                self.plugin_configuration.getboolean("question_{}".format(number), "disable_echo", default=True),
            )
        except RequiredConfigurationSettingNotFound:
            return None

    @session_cookie_property
    def questions(self):
        return {}

    def authorize(
        self,
        cookie,
        session_cookie,
        session_id,
        protocol,
        connection_name,
        client_ip,
        client_port,
        client_hostname,
        gateway_user,
        gateway_domain,
        gateway_groups,
        server_ip,
        server_port,
        server_hostname,
        server_username,
        server_domain,
        key_value_pairs
    ):
        """
        **Should not be modified.**

        The :meth:`authorize` function is called by SPS directly. Should not be modified, see
        :meth:`do_authorize` for customization.
        """

        self._setup_self(
            cookie,
            session_cookie,
            ConnectionInfo(
                session_id=session_id,
                protocol=protocol,
                connection_name=connection_name,
                client_ip=client_ip,
                client_port=client_port,
                client_hostname=client_hostname,
                gateway_username=gateway_user,
                gateway_domain=gateway_domain,
                gateway_groups=gateway_groups,
                server_ip=server_ip,
                server_port=server_port,
                server_hostname=server_hostname,
                server_username=server_username,
                server_domain=server_domain,
                key_value_pairs=key_value_pairs
            )
        )
        return self.finalize_hook(
            self._add_cookies(
                self._execute_steps(checkpoints_key="authorization_checkpoints", steps=self._authorization_steps())
            )
        )

    def session_ended(self, session_id, cookie, session_cookie):
        """
        **Should not be modified.**

        The :meth:`session_ended` function is called by SPS directly. Should not be modified, see
        :meth:`do_session_ended` for customization.
        """

        self._setup_self(cookie, session_cookie, ConnectionInfo(session_id=session_id))
        return self.finalize_hook(
            self._execute_steps(checkpoints_key="session_ended_checkpoints", steps=self._session_ended_steps())
        )

    def _setup_self(self, cookie, session_cookie, connection_info):
        self.connection = connection_info
        self.cookie = cookie
        self.session_cookie = session_cookie

    def _execute_steps(self, checkpoints_key, steps):
        checkpoints = self._get_private(checkpoints_key, {})
        try:
            for (index, step) in enumerate(steps):
                if checkpoints.get(str(index)) == step.__name__:
                    continue
                step_result = step()
                if step_result:
                    return step_result
                else:
                    checkpoints[str(index)] = step.__name__
        finally:
            self._set_private(checkpoints_key, checkpoints)
        return None

    def _add_gateway_user(self, verdict):
        """
        An ACCEPT verdict should return the username that was actually authenticated as gateway user. This function
        will use the actual self.username in the return value, unless already set by do_authenticate.

        :param verdict: an ACCEPT verdict
        :return: updated verdict
        """
        if not self._is_accept_verdict(verdict):
            return verdict
        if self.username != self.connection.gateway_user and "gateway_user" not in verdict:
            verdict["gateway_user"] = self.username
            verdict["gateway_groups"] = verdict.get("gateway_groups", self.connection.gateway_groups or ())
        return verdict

    @classmethod
    def _is_accept_verdict(cls, verdict):
        return isinstance(verdict, dict) and verdict.get("verdict") == "ACCEPT"
