#
# Copyright 2025 One Identity LLC.
# ALL RIGHTS RESERVED.
#
from safeguard.sessions.plugin.exceptions import PluginSDKRuntimeError


class LocalCredentialStoreNotFound(PluginSDKRuntimeError):
    """
    The :class:`LocalCredentialStoreNotFound` exception is raised when the configured local credential store cannot be
    found.
    """

    def __init__(self, credstore_name):
        super().__init__("Local credential store cannot be found", {"name": credstore_name})
