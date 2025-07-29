#
# Copyright 2025 One Identity LLC.
# ALL RIGHTS RESERVED.
#
"""
.. py:module:: safeguard.sessions.plugin.plugin_base
    :synopsis: Plugin base class.

The following decorators and the
:class:`PluginBase <safeguard.sessions.plugin.plugin_base.PluginBase>` class may be used in any Plugin SDK based plugin
to get some basic functionality.

"""
import os
from . import logging
from .plugin_configuration import PluginConfiguration
from .box_configuration import BoxConfiguration


class LazyProperty:
    def __init__(self, factory):
        self._factory = factory

    def __get__(self, instance, owner):
        return self.__set__(instance, self._factory(instance))

    def __set__(self, instance, value):
        instance.__dict__[self._name] = value
        return value

    __delete__ = None  # disable delete

    def __set_name__(self, owner, name):
        self._name = name


def lazy_property(factory):
    """
    The :meth:`@lazy_property <lazy_property>` decorator is used to mark attributes that should only be evaluated when
    accessed. This is useful when the calculation of the attribute is heavy, but not always necessary.

    **Usage**

    To use ``self.foobar`` as a lazy property, simply define it on the Plugin class, and decorate it with
    :meth:`@lazy_property <lazy_property>` decorator:

    .. code-block:: python

        from safeguard.sessions.plugin import AAPlugin
        from safeguard.sessions.plugin.plugin_base import lazy_property

        class MyPlugin(AAPlugin):
            @lazy_property
            def foobar(self):
                return calculate_answer()

            def do_authenticate(self):
                if need_foobar:
                    print(self.foobar)

    """
    return LazyProperty(factory)


class CookieProperty:
    def __init__(self, key, factory):
        self._key = key
        self._factory = factory

    def __get__(self, instance, owner):
        if self._key not in instance.cookie:
            instance.cookie[self._key] = self._factory(instance)
        return instance.cookie[self._key]

    def __set__(self, instance, value):
        instance.cookie[self._key] = value
        return value

    def __delete__(self, instance):
        del instance.cookie[self._key]


def cookie_property(factory):
    """
    The :meth:`@cookie_property <cookie_property>` decorator is used to mark attributes that should be passed in the
    cookie between invocations of the same plugin. Setting up such property is an easy way to store and retrieve data
    in ``self.cookie``. Similarly to :meth:`@lazy_property <lazy_property>` attributes, the evaulation of a
    :meth:`@cookie_property <cookie_property>` attribute is also delayed until usage.

    **Usage**

    To use ``self.foobar`` as a cookie property, simply define it on the Plugin class, and decorate it with
    :meth:`@cookie_property <cookie_property>` decorator:

    .. code-block:: python

        from safeguard.sessions.plugin import AAPlugin
        from safeguard.sessions.plugin.plugin_base import cookie_property

        class MyPlugin(AAPlugin):
            @cookie_property
            def foobar(self):
                return 42

            def do_authenticate(self):
                assert self.foobar == 42
                self.foobar = 0

            def do_authorize(self):
                assert self.foobar == 0

    The decorator :meth:`@cookie_property <cookie_property>` together with code in
    :class:`AAPlugin <safeguard.sessions.plugin.AAPlugin>` will ensure that ``foobar`` is stored and retrieved from
    the cookie passed to the plugin.

    The initial definition of foobar is 42 in this case, but it can be any function - this function is only called
    if foobar was not accessed before. To be more precise foobar is initialized with its factory function if it is
    being accessed and it is not present in ``self.cookie``.
    """
    return CookieProperty(factory.__name__, factory)


def named_cookie_property(key=None):
    """
    The :meth:`@named_cookie_property <named_cookie_property>` decorator is working similarly to the
    :meth:`@cookie_property <cookie_property>` decorator.
    The only difference is you can specify the key you want to save value in the ``self.cookie``
    It is important that you have to call the decorator with the desired key name, see usage.

    **Usage**

    To use ``self.my_custom_key`` as a cookie property, simply define it on the Plugin class, and decorate it with
    :meth:`@named_cookie_property(key=my_custom_key) <named_cookie_property>` decorator:

    .. code-block:: python

        from safeguard.sessions.plugin import AAPlugin
        from safeguard.sessions.plugin.plugin_base import named_cookie_property

        class MyPlugin(AAPlugin):
            @named_cookie_property(key=my_custom_key)
            def foobar(self):
                return 42

            def do_authenticate(self):
                assert self.cookie.my_custom_key == 42

    """
    return lambda factory: CookieProperty(key or factory.__name__, factory)


class SessionCookieProperty:
    def __init__(self, key, factory):
        self._key = key
        self._factory = factory

    def __get__(self, instance, owner):
        if self._key not in instance.session_cookie:
            instance.session_cookie[self._key] = self._factory(instance)
        return instance.session_cookie[self._key]

    def __set__(self, instance, value):
        instance.session_cookie[self._key] = value
        return value

    def __delete__(self, instance):
        del instance.session_cookie[self._key]


def session_cookie_property(factory):
    """
    The :meth:`@session_cookie_property <session_cookie_property>` decorator is used to mark attributes that should be
    passed in the session cookie between invocations of all plugins relevant to the session.
    Setting up such property is an easy way to store and retrieve data in ``self.session_cookie``.
    Similarly to :meth:`@lazy_property <lazy_property>` attributes, the evaulation of a
    :meth:`@session_cookie_property <session_cookie_property>` attribute is also delayed until usage.

    **Usage**

    To use ``self.foobar`` as a session cookie property, simply define it on the Plugin class, and decorate it with
    :meth:`@session_cookie_property <session_cookie_property>` decorator:

    .. code-block:: python

        from safeguard.sessions.plugin import AAPlugin
        from safeguard.sessions.plugin.plugin_base import session_cookie_property

        class MyPlugin(AAPlugin):
            @session_cookie_property
            def foobar(self):
                return 42

            def do_authenticate(self):
                assert self.foobar == 42
                self.foobar = 0

            def do_authorize(self):
                assert self.foobar == 0

    The decorator :meth:`@session_cookie_property <session_cookie_property>` together with code in
    :class:`AAPlugin <safeguard.sessions.plugin.AAPlugin>` will ensure that ``foobar`` is stored and retrieved from
    the session cookie passed to the plugin.

    The initial definition of foobar is 42 in this case, but it can be any function - this function is only called
    if foobar was not accessed before. To be more precise foobar is initialized with its factory function if it is
    being accessed and it is not present in ``self.session_cookie``.
    """
    return SessionCookieProperty(factory.__name__, factory)


class PluginBase:
    """
    The :class:`PluginBase` class is a common base class for every kind of plugins. This class is not meant to be
    used directly.

    .. py:attribute:: cookie

        The :py:attr:`self.cookie <cookie>` attribute is a dict that retains its contents between invocations of
        plugin hooks of the same plugin instance. This is the way to pass data between these functions.

    .. py:attribute:: session_cookie

        The :py:attr:`self.session_cookie <session_cookie>` is similar to :py:attr:`self.cookie <cookie>`, but it is
        also visible in other plugins in the same session.

    .. py:attribute:: plugin_configuration

        The :py:attr:`self.plugin_configuration <plugin_configuration>` attribute provides access to the plugin
        configuration via the
        :class:`PluginConfiguration <safeguard.sessions.plugin.plugin_configuration.PluginConfiguration>` class.

    .. py:attribute:: logger

        The :py:attr:`self.logger <logger>` attribute should be used to access Python logging. Its log level is
        set up from the plugin configuration.

    .. py:attribute:: https_proxy_enabled

        The :py:attr:`self.https_proxy_enabled <yes/no>` attribute enables or disables
        the HTTPS proxy which is set either system wide or in the plugin configuration via the https_proxy section.

    .. py:attribute:: https_proxy_server

        The :py:attr:`self.https_proxy_server <https_proxy_server>` attribute contains the IP address or hostname of
        the HTTPS proxy which is set either system wide or in the plugin configuration via the https_proxy section.

    .. py:attribute:: https_proxy_port

        The :py:attr:`self.https_proxy_port <https_proxy_port>` attribute contains the port number of
        the HTTPS proxy which is set either system wide or in the plugin configuration via the https_proxy section.

    .. py:attribute:: https_proxy_username

        The :py:attr:`self.https_proxy_username <https_proxy_username>` attribute contains the basic authentication
        username of
        the HTTPS proxy which is set either system wide or in the plugin configuration via the https_proxy section.

    .. py:attribute:: https_proxy_password

        The :py:attr:`self.https_proxy_password <https_proxy_password>` attribute contains the basic authentication
        password of
        the HTTPS proxy which is set either system wide or in the plugin configuration via the https_proxy section.

    .. py:attribute:: proxy_settings

        The :py:attr:`self.proxy_settings <proxy_settings>` attribute is a dictionary of the HTTPS settings.

    .. py:attribute:: box_configuration

        The :py:attr:`self.box_configuration <box_configuration>` attribute provides access to system settings.

    The :meth:`__init__` constructor method parses the configuration and sets up logging and http proxy environment
    variables.
    """

    def __init__(self, configuration, defaults=None, logger=None):
        self.cookie = None
        self.connection = None
        self.session_cookie = None
        self.plugin_configuration = PluginConfiguration(configuration, defaults=defaults)
        logging.configure(self.plugin_configuration)
        self.logger = logger or logging.get_logger(__name__)
        self.set_https_proxy()

    def finalize_hook(self, result=None):
        self.box_configuration.close()
        return result

    @lazy_property
    def box_configuration(self):
        return BoxConfiguration.open()

    @lazy_property
    def proxy_settings(self):
        if self._is_proxy_set_in_config():
            return self._override_proxy_from_config()
        else:
            return self._get_proxy_settings_from_box_config()

    @property
    def https_proxy_enabled(self):
        return self.plugin_configuration.getboolean("https_proxy", "enabled", default=True)

    @property
    def https_proxy_server(self):
        return self.proxy_settings.get("server")

    @property
    def https_proxy_port(self):
        return self.proxy_settings.get("port")

    @property
    def https_proxy_username(self):
        return self.proxy_settings.get("username")

    @property
    def https_proxy_password(self):
        return self.proxy_settings.get("password")

    def set_https_proxy(self):
        if self.https_proxy_enabled:
            https_proxy = self._calculate_http_proxy(self.proxy_settings)
            if https_proxy:
                self.logger.info(
                    "Setting HTTPS proxy server to: server={} port={}".format(
                        self.https_proxy_server, self.https_proxy_port
                    )
                )
                os.environ["https_proxy"] = os.environ["HTTPS_PROXY"] = https_proxy
                self.logger.debug("Proxy set to {}".format(os.environ["HTTPS_PROXY"]))
            else:
                self.logger.info("HTTPS proxy server enabled but not configured properly: dropping proxy")
                self.unset_https_proxy()
        else:
            self.logger.info("HTTPS proxy server is not enabled")
            self.unset_https_proxy()

    @staticmethod
    def unset_https_proxy():
        os.environ.pop("https_proxy", None)
        os.environ.pop("HTTPS_PROXY", None)

    def _get_proxy_settings_from_box_config(self):
        proxy_settings = self.box_configuration.get_http_proxy()
        return dict(
            server=proxy_settings.server,
            port=proxy_settings.port,
            username=proxy_settings.username,
            password=proxy_settings.password,
        )

    def _override_proxy_from_config(self):
        return dict(
            server=self._get_value_from_aliased_section_header("https-proxy", "server"),
            port=self._get_value_from_aliased_section_header("https-proxy", "port", self.plugin_configuration.getint)
            or 3128,
            username=self._get_value_from_aliased_section_header("https-proxy", "username"),
            password=self._get_value_from_aliased_section_header("https-proxy", "password"),
        )

    def _is_proxy_set_in_config(self):
        return self._get_value_from_aliased_section_header("https-proxy", "server") is not None

    def _get_value_from_aliased_section_header(self, header, field, getter=None):
        getter = getter or self.plugin_configuration.get
        return getter(header, field) or getter(header.replace("-", "_"), field)

    @staticmethod
    def _calculate_http_proxy(proxy_settings):
        if proxy_settings.get("server") and proxy_settings.get("port"):
            if proxy_settings.get("username") and proxy_settings.get("password"):
                auth_string = "{username}:{password}@".format(
                    username=proxy_settings["username"], password=proxy_settings["password"]
                )
            else:
                auth_string = ""
            return "https://{auth}{server}:{port}".format(
                auth=auth_string, server=proxy_settings["server"], port=proxy_settings["port"]
            )
        else:
            return None

    def _add_cookies(self, result):
        if not isinstance(result, dict):
            return result

        if "cookie" in result:
            self.cookie.update(result["cookie"])
        result["cookie"] = self.cookie

        if "session_cookie" in result:
            self.session_cookie.update(result["session_cookie"])
        result["session_cookie"] = self.session_cookie

        return result

    @cookie_property
    def __plugin_sdk_private(self):
        return {}

    def _get_private(self, key, default=None):
        return self.__plugin_sdk_private.get(key, default)

    def _set_private(self, key, value):
        self.__plugin_sdk_private[key] = value

    def _pop_private(self, key):
        value = self.__plugin_sdk_private[key]
        del self.__plugin_sdk_private[key]
        return value
