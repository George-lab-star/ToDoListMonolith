from dataclasses import dataclass
from typing import Any

from src.core.domain.entity_base import EntityBase


@dataclass
class User(EntityBase):
    """
    Domain model representing a user in the system.

    This entity encapsulates the core business attributes of a user,
    independent of how they are persisted or exposed externally.

    Attributes:
        id: Unique identifier of the user.
        name: Name of the user.
        email: Email of the user.
        hashed_password: User's hashed password.
        is_active: Indicates whether the user is currently active.
        is_superuser: Indicates whether the user has administrative privileges.
        is_verified: Indicates whether the user has verified their email address.
    """
    id: int
    name: str
    email: str
    hashed_password: str
    is_active: bool
    is_superuser: bool
    is_verified: bool
    tasks: Any = None


@dataclass
class UserCreate(EntityBase):
    """
    Domain model representing user data required for creation.

    Used to encapsulate the input necessary to create a new user in the system.

    Attributes:
        name: Name of the new user.
        email: Email of the new user.
        hashed_password: User's hashed password.
        is_active: Whether the new user should be active.
        is_superuser: Whether the user has elevated privileges.
        is_verified: Whether the user's email is verified.
    """
    name: str
    email: str
    hashed_password: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False


@dataclass
class UserUpdate(EntityBase):
    """
    Domain model for updating user information.

    Represents a partial update operation for a user entity.

    Attributes:
        id: Unique identifier of the user to be updated.
        name: New name of the user (optional).
        email: New email of the user (optional).
        hashed_password: New user's hashed password (optional).
        is_active: Whether the user should be active (optional).
        is_superuser: Whether the user should be a superuser (optional).
        is_verified: Whether the user is verified (optional).
    """
    id: int
    name: str | None = None
    email: str | None = None
    hashed_password: str | None = None
    tasks: Any = None
    is_active: bool | None = True
    is_superuser: bool | None = False
    is_verified: bool | None = False
