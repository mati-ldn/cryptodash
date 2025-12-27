import redis
import logging

logger = logging.getLogger(__name__)


def get_redis():
    try:
        client = redis.Redis(
            host="localhost",
            port=6379,
            db=0,
            socket_connect_timeout=1,
            socket_timeout=1,
        )
        client.ping()
        logger.info("Redis connected")
        return client
    except Exception as e:
        logger.warning(f"Redis unavailable, falling back to no-cache: {e}")
        return None
