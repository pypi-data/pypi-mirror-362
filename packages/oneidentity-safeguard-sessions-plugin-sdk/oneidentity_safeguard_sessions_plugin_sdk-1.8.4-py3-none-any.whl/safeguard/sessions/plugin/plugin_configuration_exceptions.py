#
# Copyright 2025 One Identity LLC.
# ALL RIGHTS RESERVED.
#
from safeguard.sessions.plugin.exceptions import PluginSDKRuntimeError


class RequiredConfigurationSettingNotFound(PluginSDKRuntimeError):
    """
    The :class:`RequiredConfigurationSettingNotFound` excpetion is raised when a required configuration option is not
    present when requested by the plugin.
    """

    pass
