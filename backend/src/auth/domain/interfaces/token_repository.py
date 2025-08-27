from abc import ABC, abstractmethod
from typing import Optional


class IRefreshTokenRepository(ABC):
    """
    Abstract base class for a refresh token repository.
    This interface defines methods for storing, retrieving, and deleting refresh tokens.

    Methods:
        store_refresh_token(user_id: int, refresh_token: str):
            Store a refresh token associated with a user ID.

        get_refresh_token(user_id: int) -> Optional[str]:
            Retrieve the refresh token associated with a user ID.
            Returns None if no token is found.

        delete_refresh_token(user_id):
            Delete the refresh token associated with a user ID.
    """

    @abstractmethod
    async def store_refresh_token(self, user_id: int, refresh_token: str):
        """
        Store a refresh token associated with a user ID.

        Args:
            user_id (int): The ID of the user to associate with the refresh token.
            refresh_token (str): The refresh token to store.
        """
        pass

    @abstractmethod
    async def get_refresh_token(self, user_id: int) -> Optional[str]:
        """
        Retrieve the refresh token associated with a user ID.

        Args:
            user_id (int): The ID of the user whose refresh token is to be retrieved.

        Returns:
            Optional[str]: The refresh token if found, otherwise None.
        """
        pass
    
    @abstractmethod
    async def delete_refresh_token(self, user_id):
        """
        Delete the refresh token associated with a user ID.

        Args:
            user_id (int): The ID of the user whose refresh token is to be deleted.
        """
        pass
