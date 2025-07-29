#
# Copyright 2025 One Identity LLC.
# ALL RIGHTS RESERVED.
#
"""
.. py:module:: safeguard.sessions.plugin.memory_cache
    :synopsis: Interface to a non-persistent key-value memory-cache

The MemoryCache implements a global key-value in memory cache which is not persisted to disk when SPS restarts. The
memory cache is common for all plugins, which means that the keys may conflict between plugins. The cache should be used
with a suitable prefix applied to the keys, such as *oneidentity:starling* which contains the vendor and product
separated by a colon (:). The time to live of a cache entry may be specified on a per usage basis or per service,
the value 0 means the entry never expires.

The cache is set up to handle plugins data specifically, which means these two use cases:

    * storing user data indefinitely, such as person - device associations,
    * storing external service data for a limited time, such as time limited access tokens for REST APIs.

In both cases the pattern is to *get* the data, then if the data existed,use it, otherwise create the data and
*set* it in the cache with or without a time to live (TTL), i.e. expire time. The *set* operation always overwrites data
and there is no delete operation.

In case the cache gets full, the least frequently used entries get evicted first. The eviction algorithm is the Redis
allkeys-lfu policy, with values lfu-log-factor = 0 and lfu-decay-time = 720. The decay time is half a day as people
typically work in day cycles, which means that people that have not logged in for days will be evicted first. Half a
day is chosen instead of a full day since a session will typically have more then one access to the cache.


Configuration example
=====================
.. code-block:: ini

    [memory-cache]
    prefix=oneidentity:starling
    ttl=300

Setting and getting values
==========================
.. code-block:: python

    from safeguard.sessions.plugin import PluginConfiguration
    from safeguard.sessions.plugin.memory_cache import MemoryCache

    class Plugin:
        def __init__(self, configuration):
            self.__config = PluginConfiguration(configuration)
            self.__mem_cache = MemoryCache.from_config(self.__config)

            cached_value = self.__mem_cache.get('foo')

            if not cached_value:
                # create the cached_value and write
                cached_value = {'bar': 42'}
                self.__mem_cache.set('foo', cached_value)

            # use the cached_value
"""
import json
from safeguard.sessions.plugin_impl.memory_cache import MemoryCache as MemoryCacheImpl


class MemoryCache:
    """
    The :class:`MemoryCache` represents access to the memory cache running on SPS.

    Do not instantiate this class via its constructor, use the :py:meth:`from_config` method instead.
    """

    def __init__(self, memory_cache, prefix, ttl):
        self._memory_cache = memory_cache
        self._prefix = prefix
        self._ttl = ttl

    @classmethod
    def from_config(cls, plugin_configuration, section="memory-cache", prefix="", ttl=0):
        """
        The :py:meth:`from_config` method can be used to initialize the memory cache service.

        :param plugin_configuration: plugin configuration object
        :type plugin_configuration: :class:`PluginConfiguration \
          <safeguard.sessions.plugin.plugin_configuration.PluginConfiguration>`
        :param str section:  name of the section where the memory cache parameters are stored
        :param str prefix: unique prefix for this cache to avoid conflict with other users, should be a colon (:)
            separated string, for example *oneidentity:starling*
        :param int ttl: time to live in seconds, 0 meaning the entry never expires
        :return: object representing the service
        :rtype: :class:`MemoryCache`
        """
        return cls(
            MemoryCacheImpl(),
            plugin_configuration.get(section, "prefix", default=prefix),
            plugin_configuration.getint(section, "ttl", default=ttl),
        )

    def set(self, key, value, ttl=None):
        """
        The :py:meth:`set` method writes a key-value to the cache, overwriting any previous value. Note: do not
        write the None value directly as the :py:meth:`get` method returns None for a cache miss.

        :param str key: will be used as key, prefix with the prefix set in the configuration
        :param value: any Python data that can be encoded to JSON
        :param int ttl: time to live in seconds, 0 meaning the entry never expires.
          None means use the configured default
        """
        self.set_string(key, json.dumps(value), ttl)

    def get(self, key):
        """
        The :py:meth:`get` method reads a key-value from the cache, returning None if the key does not exist.

        :param key: will be used as key, prefix with the prefix set in the configuration
        :return: JSON decoded value
        """
        json_data = self.get_string(key)
        return json_data and json.loads(json_data)

    def set_string(self, key, value, ttl=None, encoding="utf-8"):
        self.set_binary(key, value.encode(encoding), ttl)

    def get_string(self, key, encoding="utf-8"):
        binary_value = self.get_binary(key)
        return binary_value and binary_value.decode(encoding)

    def set_binary(self, key, value, ttl=None):
        self._memory_cache.set_binary(self._stored_key(key), value, self._ttl if ttl is None else ttl)

    def get_binary(self, key):
        return self._memory_cache.get_binary(self._stored_key(key))

    def _stored_key(self, key):
        return ":".join((self._prefix, key)) if self._prefix else key
