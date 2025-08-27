from typing import Annotated

from fastapi import Depends

from src.tasks.domain.interfaces.task_uow import ITaskUnitOfWork
from src.tasks.infrastructure.db.unit_of_work import PGTaskUnitOfWork


def get_task_uow() -> ITaskUnitOfWork:
    """
    Dependency that provides an instance of ITaskUnitOfWork.

    This allows the presentation layer to remain decoupled from the actual implementation.
    By default, it returns a PostgreSQL-based unit of work (PGTaskUnitOfWork), but the implementation
    can be easily overridden for testing or different environments.

    :return: ITaskUnitOfWork instance.
    """
    return PGTaskUnitOfWork()

TaskUoWDep = Annotated[ITaskUnitOfWork, Depends(get_task_uow)]
