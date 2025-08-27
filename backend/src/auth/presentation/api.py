from fastapi import APIRouter, Response

from src.auth.domain.dtos import AuthRequest
from src.auth.use_cases.authenticate import authenticate_user
from src.auth.use_cases.log_out import log_out
from src.auth.use_cases.refresh import refresh_token
from src.auth.presentation.dependencies import AuthDep, JWTTokenServiceDep, RefreshTokenRepositoryDep, PasswordHasherDep
from src.users.domain.dtos import UserReadDTO
from src.users.presentation.dependencies import UserUoWDep


auth_api_router = APIRouter(
    prefix="/api/auth",
    tags=[
        "auth",
    ],
)


@auth_api_router.post("/login")
async def login(
    response: Response,
    user_uow: UserUoWDep,
    pwd_hasher: PasswordHasherDep,
    token_service: JWTTokenServiceDep,
    token_repository: RefreshTokenRepositoryDep,
    user_data: AuthRequest,
):
    """
    Authenticate user and generate access and refresh tokens.
    """
    return await authenticate_user(
        response=response,
        user_data=user_data,
        set_cookies=True,
        user_uow=user_uow,
        pwd_hasher=pwd_hasher,
        token_service=token_service,
        token_repository=token_repository,
    )


@auth_api_router.post("/logout")
async def logout(
    response: Response,
    token_repository: RefreshTokenRepositoryDep,
    current_user: AuthDep,
):
    """
    Log out user by invalidating refresh token.
    """
    return await log_out(response, token_repository, current_user.id)


@auth_api_router.get("/me", response_model=UserReadDTO)
async def get_me(user_data: AuthDep):
    """
    Get current authenticated user information.
    """
    return user_data


@auth_api_router.post("/refresh")
async def refresh_token(
    response: Response,
    token_service: JWTTokenServiceDep,
    token_repository: RefreshTokenRepositoryDep,
    current_user: AuthDep,
):
    """
    Refresh access and refresh tokens using a valid refresh token.
    """
    return await refresh_token(response, token_service, token_repository, current_user)
