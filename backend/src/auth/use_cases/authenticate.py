from fastapi import Response

from src.auth.domain.dtos import AuthRequest
from src.auth.domain.exceptions import IncorrectPassword
from src.auth.domain.interfaces.token_service import ITokenService
from src.auth.domain.interfaces.token_repository import IRefreshTokenRepository
from src.users.domain.exceptions import UserNotFound
from src.users.domain.interfaces.user_uow import IUserUnitOfWork
from src.users.domain.interfaces.password_hasher import IPasswordHasher


async def authenticate_user(
    response: Response,
    user_data: AuthRequest,
    user_uow: IUserUnitOfWork,
    pwd_hasher: IPasswordHasher,
    token_service: ITokenService,
    token_repository: IRefreshTokenRepository,
    set_cookies: bool = True,
) -> dict[str, str]:
    async with user_uow:
        user = await user_uow.users.get_by_email(user_data.username)
    if not user:
        raise UserNotFound(detail=f"User with email {user_data.username} not found")
    if not pwd_hasher.verify(password=user_data.password, hashed_password=user.hashed_password):
        raise IncorrectPassword(detail=f"Incorrect password for {user_data.username}")

    access_token = token_service.create_access_token(user)
    refresh_token = token_service.create_refresh_token(user)
    await token_repository.store_refresh_token(user.id, refresh_token)

    if set_cookies:
        response.set_cookie(key="users_access_token", value=access_token, httponly=False)
        response.set_cookie(key="users_refresh_token", value=refresh_token, httponly=False)

    return {"access_token": access_token, "refresh_token": refresh_token}
