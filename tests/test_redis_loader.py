import pickle
import pandas as pd
import pytest
from cryptodash.loaders.redis_base import RedisDataFrameLoader


class FakeRedis:
    def __init__(self):
        self.store = {}

    def get(self, key):
        return self.store.get(key)

    def setex(self, key, ttl, value):
        self.store[key] = value


class TestLoader(RedisDataFrameLoader):
    def __init__(self, redis_client):
        self.redis = redis_client

    def _load(self, n=2):
        return pd.DataFrame({"x": list(range(n))})


def test_cache_miss_then_hit():
    fake_redis = FakeRedis()
    loader = TestLoader(fake_redis)

    # First call → MISS
    df1 = loader.load(n=3)
    assert len(df1) == 3

    # Second call → HIT
    df2 = loader.load(n=3)
    assert df1.equals(df2)


def test_cache_key_is_deterministic():
    loader = TestLoader(FakeRedis())

    k1 = loader._cache_key(a=1, b=2)
    k2 = loader._cache_key(b=2, a=1)

    assert k1 == k2


def test_different_args_create_different_cache():
    fake_redis = FakeRedis()
    loader = TestLoader(fake_redis)

    loader.load(n=2)
    loader.load(n=3)

    assert len(fake_redis.store) == 2
