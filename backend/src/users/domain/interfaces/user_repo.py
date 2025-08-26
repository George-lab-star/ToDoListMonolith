from abc import ABC, abstractmethod
from typing import Any

from src.users.domain.entities import User, UserCreate, UserUpdate


class IUserRepo(ABC):
    """
    Interface for user repository.

    Defines the contract for data access operations related to user entities.
    All implementations must provide persistance-specific logic for managing users.
    """

    @abstractmethod
    async def add(self, user: UserCreate) -> User:
        """
        Add a new user to the repository.

        :param user: UserCreate domain model with a user creation data.
        :return: The created User entity.
        """
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> User:
        """
        Retrieve a user by their email address.

        :param email: Email address of the user.
        :return: The matching User entity.
        """
        pass

    @abstractmethod
    async def get_by_pk(self, pk: int, to_domain: bool = True) -> Any:
        """
        Retrieve a user by their primary key.

        :param pk: Primary key (ID) of the user.
        :return: The matching User entity.
        """
        pass


    @abstractmethod
    async def update(self, user_data: UserUpdate) -> User:
        """
        Update user information.

        :param user_data: Data to update the User.
        :return: The updated User entity.
        """
        pass

    @abstractmethod
    async def delete(self, pk: int) -> None:
        """
        Delete a user by primary key.

        :param pk: Primary key (ID) of the user to delete.
        """
        pass
