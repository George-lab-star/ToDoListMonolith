from src.tasks.domain.entities import Task
from src.tasks.domain.interfaces.task_uow import ITaskUnitOfWork


async def read_task(
    task_pk: int,
    uow: ITaskUnitOfWork,
) -> Task:
    """
    Retrieve a task by its ID.

    This function fetches the task from the database and returns it.

    :param task_id: ID of the task to retrieve.
    :param uow: Unit of Work instance for handling task repository operations.
    :return: The task object.
    """
    async with uow:
        task = await uow.tasks.get_by_id(task_pk)
        return task
