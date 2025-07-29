#
# Copyright 2025 One Identity LLC.
# ALL RIGHTS RESERVED.
#
"""
.. py:module:: safeguard.sessions.plugin.logging
    :synopsis: Interface to configure and get logger objects.

Configuration example
---------------------
With this option one can set the verbosity of the logging. By default all the logs on info level will be logged to
standard error. On Safeguard for privileged sessions, the standard error will be forwarded to the system logs.

Possible log levels are the following:

- debug
- info
- warning
- error
- critical

.. code-block:: ini

    [logging]
    # One of 'debug', 'info', 'warning', 'error', 'critical'
    log_level = info

Configuring the logger service
------------------------------
.. code-block:: python

    from safeguard.sessions.plugin import logging
    from safeguard.sessions.plugin import PluginConfiguration

    class Plugin:
        def __init__(self, configuration):
            self._plugin_config = PluginConfiguration(configuration)
            logging.configure(self._plugin_config)

Acquiring a logger
------------------
.. code-block:: python

    from safeguard.sessions.plugin.logging import get_logger

    class Plugin:
        def __init__(self, configuration):
            self._log = get_logger(__name__)

Usage example
--------------
.. code-block:: python

    from safeguard.sessions.plugin import logging
    from safeguard.sessions.plugin import PluginConfiguration

    class Plugin:
        def __init__(self, configuration):
            self._plugin_config = PluginConfiguration(configuration)
            logging.configure(self._plugin_config)
            self._log = logging.get_logger(__name__)

        def do_some_logging(self):
            self._log.debug('This is a debug level log')
            self._log.info('This is an info level log')
            self._log.warning('This is a warning level log')
            self._log.error('This is an error level log')
            self._log.critical('This is a critical level log')
"""
import logging
import logging.handlers


LOG_LEVELS = ["debug", "info", "warning", "error", "critical"]
DEFAULT_LOG_LEVEL = "info"
DESTINATIONS = ["stderr", "messages"]
DEFAULT_DESTINATION = "stderr"


def get_logger(name=None):
    """
    The :meth:`get_logger` method acquires a Python Logger object of the given name.

    :param str name: name of the logger
    :return: logger with specific name
    :rtype: logger.RootLogger or logger.Logger
    """
    return logging.getLogger(name)


def configure(configuration, log_level=None):
    """
    The :meth:`configure` method sets the log level of root logger from the given plugin configuration.

    :param configuration: Configuration containing the desired log level
    :type configuration: :class:`safeguard.sessions.plugin.pluginconfig.PluginConfig`
    :param str log_level: log level to set on the root logger
    :return: None
    :rtype: NoneType
    :raises: :class:`PluginSDKValueError <safeguard.sessions.plugin.exceptions.PluginSDKValueError>`
    """
    log_level = log_level or configuration.getienum("logging", "log_level", LOG_LEVELS, default=DEFAULT_LOG_LEVEL)
    log_level_value = getattr(logging, log_level.upper())
    destination = configuration.getienum("logging", "destination", DESTINATIONS, default=DEFAULT_DESTINATION)
    root_logger = logging.getLogger()
    if destination == "messages":
        root_logger.addHandler(logging.handlers.SysLogHandler(address="/dev/log"))
    if not root_logger.handlers:
        root_logger.addHandler(logging.StreamHandler())
    root_logger.setLevel(logging.INFO)
    root_logger.info("Logging initialized to level={}".format(log_level))
    root_logger.setLevel(log_level_value)
