from typing import Optional

import redis.asyncio as aioredis

from src.auth.domain.interfaces.token_repository import IRefreshTokenRepository
from src.core.config import settings


class RedisRefreshTokenRepository(IRefreshTokenRepository):
    """
    Implementation of the IRefreshTokenRepository interface using Redis for token storage.
    
    Attributes:
        redis_client (aioredis.Redis): The Redis client used for storing and retrieving refresh tokens.
    """

    def __init__(self, redis_client: aioredis.Redis):
        """
        Initialize the RedisRefreshTokenRepository with a Redis client.

        Args:
            redis_client (aioredis.Redis): An instance of the Redis client for asynchronous operations.
        """
        self.redis_client = redis_client

    async def store_refresh_token(self, user_id: int, refresh_token: str):
        """
        Store a refresh token associated with a user ID in Redis.

        Args:
            user_id (int): The ID of the user to associate with the refresh token.
            refresh_token (str): The refresh token to store.
        """
        await self.redis_client.set(str(user_id), refresh_token, ex=settings.REFRESH_TOKEN_EXPIRE_SECONDS)

    async def get_refresh_token(self, user_id: int) -> Optional[str]:
        """
        Retrieve the refresh token associated with a user ID from Redis.

        Args:
            user_id (int): The ID of the user whose refresh token is to be retrieved.

        Returns:
            Optional[str]: The refresh token if found, otherwise None.
        """
        return await self.redis_client.get(str(user_id))
    
    async def delete_refresh_token(self, user_id: int):
        """
        Delete the refresh token associated with a user ID from Redis.

        Args:
            user_id (int): The ID of the user whose refresh token is to be deleted.
        """
        return await self.redis_client.delete(str(user_id))
