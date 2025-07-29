#
# Copyright 2025 One Identity LLC.
# ALL RIGHTS RESERVED.
#
"""
.. py:module:: safeguard.sessions.plugin.exceptions
    :synopsis: Common base classes for Plugin SDK exceptions. Provides a common way to format the text message in the
        exceptions.
"""


class PluginSDKExceptionFormatter:
    """
    The :class:`PluginSDKExceptionFormatter` is the base class for Plugin SDK exceptions.

    :param str message: free text without variables
    :param dict variables: a dictionary of variables to format in the exception message or None

    Not to be used directly, the PluginSDKExceptionFormatter adds formatting of variables provided to an exception.
    """

    def __init__(self, message, variables=None):
        self.__message = message
        self.__variables = [variables] if isinstance(variables, dict) else []
        super().__init__(message)

    def append_variables(self, variables):
        """
        The :meth:`append_variables` adds more details to an exception object. Does not overwrite previous details,
        even if the same key is used.

        :param dict variables: additional variables
        :return: self
        """
        self.__variables.append(variables) if isinstance(variables, dict) else self.__variables
        return self

    def __str__(self):
        """
        Formatting implementation.

        :return: string representation
        """
        details = ["{}='{}'".format(k, v) for variables in self.__variables for (k, v) in variables.items()]
        return self.__message + "; " + ", ".join(details) if details else self.__message


class PluginSDKRuntimeError(PluginSDKExceptionFormatter, RuntimeError):
    """
    The :class:`PluginSDKRuntimeError` is the base class for Python RuntimeError like exceptions with formatting,
    it is also a subclass of :class:`PluginSDKExceptionFormatter`.
    """

    pass


class PluginSDKRuntimeWarning(PluginSDKExceptionFormatter, RuntimeWarning):
    """
    The :class:`PluginSDKRuntimeWarning` is the base class for Python RuntimeError like exceptions with formatting,
    it is also a subclass of :class:`PluginSDKExceptionFormatter`.
    """

    pass


class PluginSDKValueError(PluginSDKExceptionFormatter, ValueError):
    """
    The :class:`PluginSDKValueError` is the base class for Python RuntimeError like exceptions with formatting,
    it is also a subclass of :class:`PluginSDKExceptionFormatter`.
    """

    pass
