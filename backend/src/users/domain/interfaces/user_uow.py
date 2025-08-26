from abc import ABC, abstractmethod

from src.users.domain.interfaces.user_repo import IUserRepo


class IUserUnitOfWork(ABC):
    """
    Unit of Work for managing user-relaated operations.

    This interface defines the transactional boundary for operations on the user repository.
    It ensures that changes are commited or rolled back as a single unit.

    Attributes:
        users: The repository interface for user operations.
    """

    users: IUserRepo

    async def __aenter__(self):
        """
        Enter the Unit of Work context.

        :return: The Unit of Work instance.
        """
        return self
    
    async def __aexit__(self, *args):
        """
        Exit the Unit of Work context, rolling back any uncommited changes.
        """
        await self.rollback()

    async def commit(self):
        """
        Commit all pending changes in the Unit of Work.
        """
        await self._commit()

    @abstractmethod
    async def rollback(self):
        """
        Roll back any uncommited changes in the Unit of Work.
        """
        pass

    @abstractmethod
    async def _commit(self):
        """
        Internal commit implementation.
        """
        pass