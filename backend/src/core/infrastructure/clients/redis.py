import redis.asyncio as aioredis
from functools import lru_cache

from src.core.config import settings


@lru_cache
def get_redis_client() -> aioredis.Redis:
    """
    Create and cache a Redis client instance.

    This function initializes a singleton Redis connection using the provided redis_url
    from settings. The use of `lru_cache` ensures that only one Redis connection
    is created and reused throughout the application lifetime.

    :return: A cached Redis client instance.
    """
    return aioredis.from_url(
        url=settings.redis_url,
        decode_responses=True,
        encoding="utf-8"
    )
