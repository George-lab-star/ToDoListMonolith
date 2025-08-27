import datetime
from typing import Annotated

from fastapi import Cookie, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer

from src.users.domain.entities import User
from src.core.config import settings
from src.core.infrastructure.clients.redis import get_redis_client
from src.auth.domain.interfaces.token_service import ITokenService
from src.auth.domain.interfaces.token_repository import IRefreshTokenRepository
from src.auth.infrastructure.jwt_service import JWTTokenService
from src.auth.infrastructure.redis_refresh_repo import RedisRefreshTokenRepository
from src.users.domain.interfaces.password_hasher import IPasswordHasher
from src.users.infrastructure.services.password_hasher import BcryptPasswordHasher
from src.users.presentation.dependencies import get_user_uow


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/auth/login",
    scheme_name="JWT",
)


def get_jwt_service() -> ITokenService:
    """
    Dependency provider for jwt token service.

    Returns an instance of `ITokenService` implemented using the jose library.
    This function is intended to be used as a dependency injection entry point
    in application or presentation layers.

    :return: A token service instance conforming to the `ITokenService` interface.
    """
    return JWTTokenService(
        secret_key=settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM,
        access_token_expires_sec=settings.ACCESS_TOKEN_EXPIRE_SECONDS,
        refresh_token_expires_sec=settings.REFRESH_TOKEN_EXPIRE_SECONDS,
    )


def get_token_repository() -> IRefreshTokenRepository:
    """
    Dependency provider for token repository.

    Returns an instance of `IRefreshTokenRepository` implemented using the redis.asyncio.
    This function is intended to be used as a dependency injection entry point
    in application or presentation layers.

    :return: A token repository instance conforming to the `IRefreshTokenRepository` interface.
    """
    return RedisRefreshTokenRepository(
        redis_client=get_redis_client()
    )


def get_password_hasher() -> IPasswordHasher:
    """
    Dependency provider for password hashing service.

    Returns an instance of `IPasswordHasher` implemented using the Bcrypt algorithm.
    This function is intended to be used as a dependency injection entry point
    in application or presentation layers.

    :return: A password hasher instance conforming to the `IPasswordHasher` interface.
    """
    return BcryptPasswordHasher()


async def get_current_user(access_token: str = Cookie(None, alias="users_access_token"), refresh_token: str = Cookie(None, alias="users_refresh_token"), jwt_token_service: ITokenService = Depends(get_jwt_service)):
    """
    Dependency function to get the current authenticated user from the access token.
    
    Args:
        token (str, optional): The JWT access token extracted from the 'users_access_token' cookie.
        jwt_token_service (ITokenService): The token service dependency for decoding tokens.
    
    Returns:
        User: The authenticated user object.
    
    Raises:
        HTTPException: 
            - 403 Forbidden if no token is provided.
            - 401 Unauthorized if token is expired, invalid, or user not found.
    """
    if not access_token and not refresh_token:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    
    payload = jwt_token_service.decode_token(access_token or refresh_token)
    expire = payload.get('exp')
    
    if expire:
        expire_time = datetime.datetime.fromtimestamp(int(expire), tz=datetime.timezone.utc)
        if (not expire) or (expire_time < datetime.datetime.now(datetime.timezone.utc)):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token expired')

        user_id = payload.get('sub')
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='ID of user not found')
        
        user_uow = get_user_uow()
        async with user_uow:
            user = await user_uow.users.get_by_pk(int(user_id))
        
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')

        return user



JWTTokenServiceDep = Annotated[ITokenService, Depends(get_jwt_service)]
RefreshTokenRepositoryDep = Annotated[IRefreshTokenRepository, Depends(get_token_repository)]
PasswordHasherDep = Annotated[IPasswordHasher, Depends(get_password_hasher)]
AuthDep = Annotated[User, Depends(get_current_user)]
