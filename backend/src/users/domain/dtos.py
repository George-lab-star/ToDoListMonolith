from typing import Any
from pydantic import BaseModel, Field, EmailStr
from src.users.domain.entities import UserUpdate


class UserReadDTO(BaseModel):
    """
    Data Transfer Object of user for reading.

    This model is designed to represent both authenticated and anonymous users,
    allowing unified usage in views like `/users/me`.

    Attributes:
        id: Unique identifier of the user (optional for anonymus users).
        name: Name of the user (optional for anonymus users).
        email: Email of the user (optional for anonymus users).
        is_active: Whether the user account is active.
        is_superuser: Whether the user has administrative privileges.
        is_verified: Whether the user has verified their email.
    """
    id: int | None
    name: str | None
    email: EmailStr | None
    tasks: Any = None
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False


class UserCreateDTO(BaseModel):
    """
    Data Transfer Object for creating user.

    This model is used when registering a new user.

    Attributes:
        name: Name of user.
        email: Email of user).
        password: User's password (length 6-120).
    """
    name: str
    email: EmailStr
    password: str = Field(min_length=6, max_length=50)
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False


class UserUpdateDTO(BaseModel):
    """
    Data Transfer Object for updating user information.

    This model is used in endpoints for partial updates to user data.

    Attributes:
        name: New name of the user (optional).
        email: New email of the user (optional).
        password: New user's password (optional).
        is_active: Whether the user account is active.
        is_superuser: Whether the user has administrative privileges.
        is_verified: Whether the user has verified their email.
    """
    name: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    is_active: bool | None = True
    is_superuser: bool | None = False
    is_verified: bool | None = False
