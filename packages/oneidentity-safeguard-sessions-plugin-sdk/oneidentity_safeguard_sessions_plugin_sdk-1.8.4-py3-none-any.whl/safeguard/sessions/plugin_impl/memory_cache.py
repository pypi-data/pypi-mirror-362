#
# Copyright 2025 One Identity LLC.
# ALL RIGHTS RESERVED.
#
import fakeredis


class FakeRedisCache:
    _redis = None

    def set_binary(self, key, value, ttl):
        self._ensure_redis()
        self._redis.set(key, value, ex=None if ttl <= 0 else ttl)

    def get_binary(self, key):
        self._ensure_redis()
        return self._redis.get(key)

    def _ensure_redis(self):
        if self._redis is None:
            self._redis = fakeredis.FakeStrictRedis()


class MemoryCache(FakeRedisCache):
    pass
