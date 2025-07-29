#
# Copyright 2025 One Identity LLC.
# ALL RIGHTS RESERVED.
#
"""
.. py:module:: safeguard.sessions.plugin.plugin_context
    :synopsis: Helps access the plugin's context.

    .. code-block:: python
        import os
        from safeguard.sessions.plugin import DEFAULT_PLUGIN_CONTEXT

        with open(os.path.join(DEFAULT_PLUGIN_CONTEXT.persistent_plugin_state_directory, 'state.dat')) as state_file:
            # read state file here ...
"""

from functools import wraps
import os
from tempfile import gettempdir


def _ensure_directory_exists(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        dir_path = func(*args, **kwargs)
        os.makedirs(dir_path, mode=0o750, exist_ok=True)
        return dir_path

    return wrapper


class PluginContext:
    """
    This class provides members through which the plugin's context can be accessed.
    """

    @property
    @_ensure_directory_exists
    def persistent_plugin_state_directory(self):
        """
        Path to a directory specific to an instance of a plugin whose contents
        are stored persistently.
        """
        return os.environ["SCB_PLUGIN_STATE_DIRECTORY"]

    @property
    @_ensure_directory_exists
    def ephemeral_plugin_state_directory(self):
        """
        Path to a directory specific to an instance of a plugin whose contents
        will be deleted when connections are suddenly lost (e.g. on system restart).
        """
        tempdir = gettempdir()
        plugin_instance_dir_name = os.path.basename(os.path.normpath(self.persistent_plugin_state_directory))
        default = os.path.join(tempdir, "ephemeral_plugin_state", plugin_instance_dir_name)

        return os.environ.get("EPHEMERAL_PLUGIN_STATE_DIRECTORY", default)


DEFAULT_PLUGIN_CONTEXT = PluginContext()
