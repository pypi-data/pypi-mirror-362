#
# Copyright 2025 One Identity LLC.
# ALL RIGHTS RESERVED.
#
import json
import os
from . import DEFAULT_PLUGIN_CONTEXT, logging
from .lockfile import lockfile_for


class NoopConnectionLimiter:
    @classmethod
    def active(cls):
        return False

    @classmethod
    def try_connect(cls, **kwargs):
        return True

    @classmethod
    def disconnect(self):
        pass


class ConnectionLimiter:
    def __init__(self, state_file_path, limit=0, lock_timeout=1, lock_retries=4, limit_description=None):
        self.__logger = logging.get_logger(__name__)
        self.state_file_path = state_file_path
        self.limit = limit
        self.__lock_timeout = lock_timeout
        self.__lock_retries = lock_retries
        self.limit_description = limit_description

        os.makedirs(os.path.dirname(self.state_file_path), mode=0o750, exist_ok=True)

        self.__logger.debug("Created directory for connection limiter: %s", os.path.dirname(self.state_file_path))

    @classmethod
    def active(cls):
        return True

    @classmethod
    def from_config(
        cls, plugin_config, keys, section="connection_limiter", plugin_context=None, limit_description=None
    ):
        limit = plugin_config.getint(section, "limit", 0)

        if limit == 0:
            return NoopConnectionLimiter()

        if plugin_context is None:
            plugin_context = DEFAULT_PLUGIN_CONTEXT
        state_file_path = os.path.join(plugin_context.ephemeral_plugin_state_directory, section, "_".join(keys))
        return cls(state_file_path=state_file_path, limit=limit, limit_description=limit_description)

    def try_connect(self, session_id):
        self.__logger.debug("Checking connection limit for session: %s", session_id)
        with lockfile_for(self.state_file_path, timeout=self.__lock_timeout, retries=self.__lock_retries):
            connections = []
            try:
                with open(self.state_file_path, "r") as state_file:
                    connections = json.load(state_file)
            except FileNotFoundError:
                self.__logger.debug("Connection state file not found: %s", self.state_file_path)
            except json.JSONDecodeError as ex:
                self.__logger.debug("Couldn't load connections from state file: %s; error=%s", self.state_file_path, ex)

            # TODO: check connections list for stale items

            if len(connections) < self.limit:
                self.__logger.debug("Connection within limit.")
                with open(self.state_file_path, "w") as state_file:
                    json.dump(connections + [session_id], state_file)
                return True
            else:
                self.__logger.info(
                    "Connection exceeding limit."
                    if self.limit_description is None
                    else ("Connection exceeding limit for: %s" % self.limit_description)
                )
                return False

    def disconnect(self, session_id):
        self.__logger.debug("Disconnecting limit for session: %s", session_id)
        with lockfile_for(self.state_file_path, timeout=self.__lock_timeout, retries=self.__lock_retries):
            with open(self.state_file_path, "r") as state_file:
                connections = json.load(state_file)
            if len(connections) < 1:
                self.__logger.warning("Disconnecting while connection limiter state indicates no connections.")
            with open(self.state_file_path, "w") as state_file:
                json.dump(list(set(connections) - {session_id}), state_file)
