from unittest.mock import MagicMock

import pytest

from src.users.use_cases.user_registration import register_user
from src.users.use_cases.user_profile import get_user_profile
from src.users.use_cases.user_update import update_user
from src.users.use_cases.user_delete import delete_user
from src.users.domain.dtos import UserCreateDTO, UserUpdateDTO
from src.users.domain.entities import User
from src.users.domain.exceptions import UserNotFound
from src.users.domain.interfaces.user_uow import IUserUnitOfWork
from src.users.domain.interfaces.password_hasher import IPasswordHasher


user_create_dto = UserCreateDTO(
    name="username",
    email="user@example.com",
    password="securepassword",
    is_active=True,
    is_superuser=False,
    is_verified=False
)


mock_hasher = MagicMock()
mock_hasher.hash = MagicMock()
mock_hasher.hash.return_value = 'hashed_secure_pwd'


@pytest.mark.asyncio
async def test_register_user(fake_user_uow: IUserUnitOfWork):
    """
    Test that a user can be successfully registered.
    """
    await _register_user(fake_user_uow)


@pytest.mark.asyncio
async def test_get_user_profile(fake_user_uow: IUserUnitOfWork):
    """
    Test retrieving a user profile by ID.

    Verifies that a registered user's profile is returned correctly,
    and that requesting a non-existent user raises UserNotFound.
    """
    user = await _register_user(fake_user_uow)
    result = await get_user_profile(user_pk=user.id, uow=fake_user_uow)
    assert result.id == 1
    assert result.email == user_create_dto.email

    with pytest.raises(UserNotFound) as exc:
         await get_user_profile(user_pk=-1, uow=fake_user_uow)
    print(exc.value.detail)
    assert exc.type is UserNotFound


@pytest.mark.asyncio
async def test_update_user(fake_user_uow: IUserUnitOfWork, fake_password_hasher: IPasswordHasher):
    """
    Test updating a user's email.

    Verifies that the email is updated correctly, and that updating
    a non-existent user raises UserNotFound.
    """
    user = await _register_user(fake_user_uow)

    update_data = UserUpdateDTO(email="user_new@example.com")
    new_user = await update_user(user_pk=user.id, user_data=update_data, pwd_hasher=fake_password_hasher, uow=fake_user_uow)
    assert new_user.id == user.id
    assert new_user.email == update_data.email

    with pytest.raises(UserNotFound) as exc:
        await update_user(user_pk=-1, user_data=update_data, pwd_hasher=mock_hasher, uow=fake_user_uow)
    assert exc.type is UserNotFound


@pytest.mark.asyncio
async def test_delete_user(fake_user_uow: IUserUnitOfWork):
    """
    Test deleting a user by ID.

    Ensures that deletion returns None and that deleting
    the same user again raises UserNotFound.
    """
    user = await _register_user(fake_user_uow)
    no_user = await delete_user(user_pk=user.id, uow=fake_user_uow)
    assert no_user is None

    with pytest.raises(UserNotFound) as exc:
        await delete_user(user_pk=user.id, uow=fake_user_uow)
    assert exc.type is UserNotFound


async def _register_user(user_uow: IUserUnitOfWork) -> User:
    """
    Helper function to register a user using a mocked password hasher.

    :param user_uow: Fake unit of work.
    :return: Created User entity.
    """
    user = await register_user(user_create_dto, mock_hasher, user_uow)
    assert user.email == user_create_dto.email
    return user
