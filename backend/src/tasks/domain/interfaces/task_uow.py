from abc import ABC, abstractmethod

from src.tasks.domain.interfaces.task_repo import ITaskRepo


class ITaskUnitOfWork(ABC):
    """
    Unit of Work for managing task-related operations.

    This interface defines the transactional boundary for operations on the task repository.
    It ensures that changes are committed or rolled back as a single unit.
    """

    tasks: ITaskRepo

    async def __aenter__(self):
        """
        Enter the Unit of Work context.

        :return: The Unit of Work instance.
        """
        return self

    async def __aexit__(self, *args):
        """
        Exit the Unit of Work context, rolling back any uncommitted changes.
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
        Roll back any uncommitted changes in the Unit of Work.
        """
        pass

    @abstractmethod
    async def _commit(self):
        """
        Internal commit implementation.
        """
        pass
