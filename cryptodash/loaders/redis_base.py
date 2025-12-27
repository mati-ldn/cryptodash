import pickle
import logging
import pandas as pd
from abc import ABC, abstractmethod
from typing import Any
import redis
from cryptodash.utils.logging_config import get_logger

logger = get_logger()


class RedisDataFrameLoader(ABC):
    """
    Pure Redis-backed DataFrame loader.
    No fallback logic here.
    """

    # default, in seconds
    ttl: int = 5 * 60

    def __init__(self):
        self.redis = self._create_redis_client()

    def _create_redis_client(self) -> redis.Redis:
        return redis.Redis(
            host="localhost",
            port=6379,
            db=0,
            socket_connect_timeout=1,
            socket_timeout=1,
        )

    def load(self, **kwargs) -> pd.DataFrame:
        cache_key = self._cache_key(**kwargs)

        cached = self.redis.get(cache_key)
        if cached is not None:
            logger.info(f"REDIS HIT [{cache_key}]")
            return pickle.loads(cached)

        logger.info(f"REDIS MISS [{cache_key}]")
        df = self._load(**kwargs)

        self.redis.setex(cache_key, self.ttl, pickle.dumps(df))
        logger.info(f"REDIS SET [{cache_key}] ttl={self.ttl}s")

        return df

    @abstractmethod
    def _load(self, **kwargs) -> pd.DataFrame:
        raise NotImplementedError

    def _cache_key(self, **kwargs) -> str:
        args = ",".join(f"{k}={v}" for k, v in sorted(kwargs.items()))
        return f"{self.__class__.__name__}:{args}"


class DummyPricesLoader(RedisDataFrameLoader):
    """
    Example loader that returns a dummy DataFrame.
    Useful for testing Redis caching behavior.
    """

    ttl = 30  # override TTL if desired

    def _load(self, rows: int = 3) -> pd.DataFrame:
        logger.info(f"Generating dummy dataframe with {rows} rows")

        return pd.DataFrame(
            {
                "symbol": ["BTC", "ETH", "SOL"][:rows],
                "price": [42000.0, 2300.5, 98.2][:rows],
                "change_24h": [1.5, -0.7, 3.2][:rows],
            }
        )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    loader = DummyPricesLoader()

    print("First call (MISS):")
    print(loader.load(rows=2))

    print("\nSecond call (HIT):")
    print(loader.load(rows=2))

    print("\nThird call (MISS):")
    print(loader.load(rows=3))
