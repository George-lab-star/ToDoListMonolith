from fastapi import Response

from src.users.domain.entities import User
from src.auth.domain.interfaces.token_service import ITokenService
from src.auth.domain.interfaces.token_repository import IRefreshTokenRepository


async def refresh_token(
    response: Response,
    token_service: ITokenService,
    token_repository: IRefreshTokenRepository,
    current_user: User,
):
    """
    Refresh access and refresh tokens using a valid refresh token.
    
    Args:
        response (Response): The FastAPI response object to set cookies.
        token_service (JWTTokenServiceDep): The token service dependency.
        token_repository (RefreshTokenRepositoryDep): The refresh token repository dependency.
        user_uow (UserUoWDep): The user unit of work dependency.
        current_user (User): The current authenticated user from the refresh token.
    
    Returns:
        dict: A dictionary containing the new access token.
    
    Raises:
        HTTPException: 401 Unauthorized if refresh token is invalid or user not found.
    """
    new_access_token = token_service.create_access_token(current_user)
    
    new_refresh_token = token_service.create_refresh_token(current_user)
    await token_repository.store_refresh_token(current_user.id, new_refresh_token)
    
    response.set_cookie(
        key="users_access_token",
        value=new_access_token,
        httponly=True,
        secure=True,
        samesite="lax"
    )
    response.set_cookie(
        key="users_refresh_token",
        value=new_refresh_token,
        httponly=True,
        secure=True,
        samesite="lax"
    )
    
    return {"access_token": new_access_token, "refresh_token": new_refresh_token}
