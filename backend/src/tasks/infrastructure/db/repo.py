from typing import List

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.tasks.domain.entities import Task, TaskCreate, TaskUpdate
from src.tasks.domain.exceptions import TaskNotFound, TaskAlreadyExists
from src.tasks.domain.interfaces.task_repo import ITaskRepo
from src.tasks.infrastructure.db.orm import DBTask, TaskStatus
from src.users.domain.interfaces.user_uow import IUserUnitOfWork


class PGTaskRepo(ITaskRepo):
    """
    PostgreSQL implementation of the task repository interface.

    This class handles CRUD operations for tasks using SQLAlchemy and a PostgreSQL database.

    Attributes:
        session (AsyncSession): The database session used for all operations.
    """

    def __init__(self, session: AsyncSession) -> None:
        """
        Initialize the repository with an active database session.

        :param session: Async SQLAlchemy session.
        """
        self.session = session

    async def add(self, task: TaskCreate, user_uow: IUserUnitOfWork) -> Task:
        """
        Create a new task in the database.

        :param task: Domain model representing the task to be created.
        :return: The created task as a domain model.
        :raises TaskAlreadyExists: if a task with the same unique fields already exists.
        """
        async with user_uow:
            owner = await user_uow.users.get_by_pk(task.owner_id, to_domain=False)
        obj = DBTask(**task.dict, owner=owner)
        self.session.add(obj)

        try:
            await self.session.flush()
        except IntegrityError as e:
            await self.session.rollback()
            raise TaskAlreadyExists(detail=str(e.orig))

        return self._to_domain(obj)

    async def get_by_id(self, task_id: int) -> Task:
        """
        Return a task by primary key (ID).

        :param pk: Task ID.
        :return: The retrieved task as a domain model.
        :raises TaskNotFound: If no task with the given ID exists.
        """
        obj: DBTask | None = await self.session.get(DBTask, task_id)
        if not obj:
            raise TaskNotFound(detail=f"Task with id {task_id} not found")

        return self._to_domain(obj)

    async def update(self, task: TaskUpdate) -> Task:
        """
        Update task fields based on input data.

        :param task_data: Domain model containing updated task fields.
        :return: Updated task as a domain model.
        :raises TaskNotFound: If the task with the specified ID does not exist.
        """
        stmt = select(DBTask).where(DBTask.id == task.id)
        result = await self.session.execute(stmt)
        obj: DBTask | None = result.scalar_one_or_none()

        if not obj:
            raise TaskNotFound(detail=f"Task with id {task.id} not found")
        
        print(task.dict)
        for field, value in task.dict.items():
            if value is not None:
                if field == 'status':
                    value = TaskStatus[value]
                setattr(obj, field, value)

        await self.session.flush()

        return self._to_domain(obj)

    async def delete(self, task_id: int) -> None:
        """
        Delete a task by primary key (ID).

        :param pk: ID of the task to delete.
        :raises TaskNotFound: If the task with the given ID does not exist.
        """
        obj = await self.session.get(DBTask, task_id)
        if not obj:
            raise TaskNotFound(detail=f"Task with id {task_id} not found")

        await self.session.delete(obj)
        await self.session.flush()

    @staticmethod
    def _to_domain(obj: DBTask) -> Task:
        return Task(
            id=obj.id,
            title=obj.title,
            description=obj.description,
            status=obj.status.value,  # Convert Enum to string
            created_at=obj.created_at,
            updated_at=obj.updated_at,
            owner_id=obj.owner_id,
        )
