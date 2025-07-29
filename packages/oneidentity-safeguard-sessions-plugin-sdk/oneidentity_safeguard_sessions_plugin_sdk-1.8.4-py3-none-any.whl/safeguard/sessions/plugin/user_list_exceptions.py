#
# Copyright 2025 One Identity LLC.
# ALL RIGHTS RESERVED.
#
from safeguard.sessions.plugin.exceptions import PluginSDKRuntimeError


class LocalUserListNotFound(PluginSDKRuntimeError):
    """
    The :class:`LocalUserListNotFound` exception is raised when the configured local user list cannot be found.
    """

    def __init__(self, user_list_name):
        super().__init__("Local user list cannot be found", {"name": user_list_name})
