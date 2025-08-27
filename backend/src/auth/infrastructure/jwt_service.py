import datetime

from fastapi import status
from fastapi.exceptions import HTTPException
from jose import JWTError, jwt

from src.auth.domain.exceptions import TokenExpired
from src.auth.domain.interfaces.token_service import ITokenService
from src.users.domain.entities import User


class JWTTokenService(ITokenService):
    """
    Implementation of the ITokenService interface using JWT for token management.
    
    Attributes:
        secret_key (str): The secret key used for encoding and decoding tokens.
        algorithm (str): The algorithm used for encoding tokens.
        access_token_expires_sec (int): The expiration time for access tokens in seconds.
        refresh_token_expires_sec (int): The expiration time for refresh tokens in seconds.
    """

    def __init__(self, secret_key: str, algorithm: str, access_token_expires_sec: int, refresh_token_expires_sec: int):
        """
        Initialize the JWTTokenService with the required parameters.

        Args:
            secret_key (str): The secret key used for encoding and decoding tokens.
            algorithm (str): The algorithm used for encoding tokens.
            access_token_expires_sec (int): The expiration time for access tokens in seconds.
            refresh_token_expires_sec (int): The expiration time for refresh tokens in seconds.
        """
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_token_expires_sec = access_token_expires_sec
        self.refresh_token_expires_sec = refresh_token_expires_sec

    def create_access_token(self, user: User) -> str:
        """
        Create a new access token for the specified user.

        Args:
            user (User ): The user for whom the access token is to be created.

        Returns:
            str: The generated access token.
        """
        expires = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=self.access_token_expires_sec)
        to_encode = {"sub": str(user.id), "exp": expires}
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

    def create_refresh_token(self, user: User) -> str:
        """
        Create a new refresh token for the specified user.

        Args:
            user (User ): The user for whom the refresh token is to be created.

        Returns:
            str: The generated refresh token.
        """
        expires = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=self.refresh_token_expires_sec)
        to_encode = {"sub": str(user.id), "exp": expires}
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
    
    def decode_token(self, token: str):
        """
        Decode a given JWT token and return its payload.

        Args:
            token (str): The token to decode.

        Returns:
            dict: The decoded token payload.

        Raises:
            HTTPException: If the token is invalid or expired.
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except JWTError as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Error: {e}")
