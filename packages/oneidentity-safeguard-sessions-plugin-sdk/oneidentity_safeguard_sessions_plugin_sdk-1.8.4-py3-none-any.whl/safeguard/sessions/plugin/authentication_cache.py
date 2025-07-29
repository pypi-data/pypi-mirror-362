#
# Copyright 2025 One Identity LLC.
# ALL RIGHTS RESERVED.
#
import json
import os
import time
from . import DEFAULT_PLUGIN_CONTEXT, logging
from .lockfile import lockfile_for
from collections import namedtuple
from functools import wraps
from sys import version_info


if version_info[:2] < (3, 7):
    # defaults for namedtuple got introduced only in Python 3.7
    namedtuple_without_defaults = namedtuple

    @wraps(namedtuple_without_defaults)
    def shim(*args, **kwargs):
        defaults = kwargs.pop("defaults", None)
        cls = namedtuple_without_defaults(*args, **kwargs)
        cls.__new__.__defaults__ = defaults
        return cls

    namedtuple = shim

DEFAULT_SOFT_TIMEOUT = 15
DEFAULT_HARD_TIMEOUT = 90
DEFAULT_REUSE_LIMIT = 0

AuthCacheLimits = namedtuple(
    "AuthCacheLimits",
    field_names=("soft_timeout", "hard_timeout", "reuse_limit"),
    defaults=(DEFAULT_SOFT_TIMEOUT, DEFAULT_HARD_TIMEOUT, DEFAULT_REUSE_LIMIT),
)


AuthCacheState = namedtuple(
    "AuthCacheState", field_names=("last_authenticated", "last_used", "reuse_count"), defaults=(0,)
)


class NoopAuthenticationCache:
    def __init__(self):
        self.log = logging.get_logger(__name__)

    def try_authenticate(self, **kwargs):
        self.log.debug("Authentication cache is turned off with 0 reuse limit")

    def cache_authentication(self, **kwargs):
        pass


class AuthenticationCache:
    def __init__(self, cache_file_path, limits=AuthCacheLimits()):
        self.log = logging.get_logger(__name__)
        self.cache_file_path = cache_file_path
        self.limits = limits

        self.__lock_timeout = 1
        self.__lock_retries = 4

        self.log.debug(
            "Initialized auth cache: %s; soft timeout: %s; hard timeout: %s; reuse limit: %s",
            self.cache_file_path,
            self.limits.soft_timeout,
            self.limits.hard_timeout,
            self.limits.reuse_limit,
        )

    @classmethod
    def from_config(cls, plugin_config, client_ip, username, section="authentication_cache", plugin_state_dir=None):
        limits = AuthCacheLimits(
            soft_timeout=plugin_config.getfloat(section, "soft_timeout", DEFAULT_SOFT_TIMEOUT),
            hard_timeout=plugin_config.getfloat(section, "hard_timeout", DEFAULT_HARD_TIMEOUT),
            reuse_limit=plugin_config.getint(section, "reuse_limit", DEFAULT_REUSE_LIMIT),
        )
        if limits.reuse_limit == 0:
            return NoopAuthenticationCache()

        if plugin_state_dir is None:
            plugin_state_dir = DEFAULT_PLUGIN_CONTEXT.persistent_plugin_state_directory
        cache_file_path = os.path.join(
            plugin_state_dir,
            plugin_config.get(section, "cache_dir", "auth_cache"),
            "{}@{}.cache".format(username, client_ip),
        )

        os.makedirs(os.path.dirname(cache_file_path), mode=0o750, exist_ok=True)

        logging.get_logger(__name__).debug("Created directory for auth cache: %s", os.path.dirname(cache_file_path))

        return cls(cache_file_path, limits)

    def try_authenticate(self, timestamp=None):
        if timestamp is None:
            timestamp = time.time()
        self.log.debug("Trying to authenticate with auth cache at %s", timestamp)
        with lockfile_for(self.cache_file_path, timeout=self.__lock_timeout, retries=self.__lock_retries):
            state = self.__get_state()
            if state is None:
                self.log.debug("No cached authentication exists.")
            elif state.last_authenticated + self.limits.hard_timeout < timestamp:
                self.log.debug("Authentication cache hard timeout reached.")
            elif state.last_used + self.limits.soft_timeout < timestamp:
                self.log.debug("Authentication cache soft timeout reached.")
            elif state.reuse_count + 1 > self.limits.reuse_limit >= 0:
                self.log.debug("Authentication cache reuse limit reached.")
            else:
                self.__set_state(state._replace(last_used=timestamp, reuse_count=state.reuse_count + 1))
                return True
        return False

    def cache_authentication(self, timestamp=None):
        if timestamp is None:
            timestamp = time.time()
        self.log.debug("Caching authentication at %s", timestamp)
        with lockfile_for(self.cache_file_path, timeout=self.__lock_timeout, retries=self.__lock_retries):
            self.__set_state(AuthCacheState(last_authenticated=timestamp, last_used=timestamp))

    def __get_state(self):
        try:
            with open(self.cache_file_path, "r") as cache_file:
                return AuthCacheState(**json.load(cache_file))
        except BaseException:
            return None

    def __set_state(self, state):
        with open(self.cache_file_path, "w") as cache_file:
            json.dump(state._asdict(), cache_file)
