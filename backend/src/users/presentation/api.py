from fastapi import APIRouter

from src.users.domain.entities import User
from src.auth.presentation.dependencies import AuthDep, PasswordHasherDep
from src.users.use_cases.user_delete import delete_user
from src.users.use_cases.user_profile import get_user_profile
from src.users.use_cases.user_registration import register_user
from src.users.use_cases.user_update import update_user
from src.users.domain.dtos import UserCreateDTO, UserUpdateDTO, UserReadDTO
from src.users.presentation.dependencies import UserUoWDep


user_api_router = APIRouter(prefix='/api/users', tags=["users"])


@user_api_router.post("", response_model=UserReadDTO, status_code=201)
async def register(user_data: UserCreateDTO, pwd_hasher: PasswordHasherDep, uow: UserUoWDep):
    """
    Register a new user.
    """
    return await register_user(user_data, pwd_hasher=pwd_hasher, uow=uow)


@user_api_router.get("/{user_id}", response_model=UserReadDTO)
async def get_profile(user_id: int, uow: UserUoWDep, user: AuthDep):
    """
    Get user profile by ID.
    """
    return await get_user_profile(user_id, uow=uow)


@user_api_router.patch("/{user_id}", response_model=UserReadDTO)
async def update(user_id: int, user_data: UserUpdateDTO, pwd_hasher: PasswordHasherDep, uow: UserUoWDep, user: AuthDep):
    """
    Update user data.
    """
    return await update_user(user_id, user_data, pwd_hasher, uow=uow)


@user_api_router.delete("/{user_id}", status_code=204)
async def delete(user_id: int, uow: UserUoWDep, user: AuthDep):
    """
    Delete user by ID.
    """
    return await delete_user(user_id, uow=uow)