from fastapi import Depends, Response
from src.auth.presentation.dependencies import get_current_user
from src.users.domain.entities import User
from src.auth.domain.interfaces.token_repository import IRefreshTokenRepository


async def log_out(
    response: Response,
    token_repository: IRefreshTokenRepository,
    current_user_id: int
) -> dict[str, str]:
    response.delete_cookie(key="users_access_token")
    response.delete_cookie(key="users_refresh_token")
    await token_repository.delete_refresh_token(current_user_id)
    return {"detail": "Successfully logged out"}
