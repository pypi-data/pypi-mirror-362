#
# Copyright 2025 One Identity LLC.
# ALL RIGHTS RESERVED.
#
"""
.. py:module:: safeguard.sessions.plugin.lazy_proxy
    :synopsis: Utility for wrapping lazily created objects.
"""


class LazyProxy:
    """
    The :class:`LazyProxy` class represents an object proxy that acts like its wrapped value which is created on-demand.
    """

    _UNDEFINED = object()

    def __init__(self, value_factory):
        if not callable(value_factory):
            raise TypeError("'value_factory' is not callable")
        self._value_factory = value_factory
        self._value = self._UNDEFINED

    def __getattr__(self, name):
        if self._value is self._UNDEFINED:
            self._value = self._value_factory()
        return getattr(self._value, name)
