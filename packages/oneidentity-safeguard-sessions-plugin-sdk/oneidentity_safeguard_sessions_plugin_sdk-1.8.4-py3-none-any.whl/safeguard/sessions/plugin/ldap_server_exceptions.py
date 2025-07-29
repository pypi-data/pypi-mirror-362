#
# Copyright 2025 One Identity LLC.
# ALL RIGHTS RESERVED.
#
from safeguard.sessions.plugin.exceptions import PluginSDKRuntimeError


class LDAPOperationError(PluginSDKRuntimeError):
    """
    The :class:`LDAPOperationError` exception is raised when an LDAP error is detected.
    """

    pass


class LDAPUserNotFound(PluginSDKRuntimeError):
    """
    The :class:`LDAPUserNotFound` exception is raised when a user is not found in the LDAP server.
    """

    def __init__(self, variables):
        super().__init__("User not found", variables)
