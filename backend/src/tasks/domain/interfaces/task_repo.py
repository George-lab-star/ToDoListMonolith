from abc import ABC, abstractmethod
from typing import List

from src.tasks.domain.entities import Task, TaskCreate, TaskUpdate
from src.users.domain.interfaces.user_uow import IUserUnitOfWork


class ITaskRepo(ABC):
    """
    Interface for task repository.

    Defines the contract for data access operations related to task entities.
    All implementations must provide persistence-specific logic for managing tasks.
    """

    @abstractmethod
    async def add(self, task: TaskCreate, user_uow: IUserUnitOfWork) -> Task:
        """
        Add a new task to the repository.

        :param task: Task entity to be added.
        :return: The created Task entity.
        """
        pass

    @abstractmethod
    async def get_by_id(self, task_id: int) -> Task:
        """
        Retrieve a task by its ID.

        :param task_id: ID of the task.
        :return: The matching Task entity.
        """
        pass

    @abstractmethod
    async def update(self, task: TaskUpdate) -> Task:
        """
        Update task information.

        :param task: Task entity with updated data.
        :return: The updated Task entity.
        """
        pass

    @abstractmethod
    async def delete(self, task_id: int) -> None:
        """
        Delete a task by ID.

        :param task_id: ID of the task to delete.
        """
        pass
