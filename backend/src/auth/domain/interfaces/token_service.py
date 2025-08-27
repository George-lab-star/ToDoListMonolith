from abc import ABC, abstractmethod
from typing import Any

from src.users.domain.entities import User


class ITokenService(ABC):
    """
    Abstract base class for a token service.
    This interface defines methods for creating and decoding access and refresh tokens.

    Methods:
        create_access_token(user: User) -> str:
            Create an access token for the specified user.

        create_refresh_token(user: User) -> str:
            Create a refresh token for the specified user.

        decode_token(token: str) -> dict[str, Any]:
            Decode a given token and return its payload as a dictionary.
    """

    @abstractmethod
    def create_access_token(self, user: User) -> str:
        """
        Create an access token for the specified user.

        Args:
            user (User ): The user for whom the access token is to be created.

        Returns:
            str: The generated access token.
        """
        pass
    
    @abstractmethod
    def create_refresh_token(self, user: User) -> str:
        """
        Create a refresh token for the specified user.

        Args:
            user (User ): The user for whom the refresh token is to be created.

        Returns:
            str: The generated refresh token.
        """
        pass

    @abstractmethod
    def decode_token(self, token: str) -> dict[str, Any]:
        """
        Decode a given token and return its payload as a dictionary.

        Args:
            token (str): The token to decode.

        Returns:
            dict[str, Any]: The decoded token payload.
        """
        pass
