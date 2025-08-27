from src.tasks.domain.entities import Task, TaskUpdate
from src.tasks.domain.interfaces.task_uow import ITaskUnitOfWork
from src.tasks.domain.dtos import TaskUpdateDTO
from src.tasks.domain.exceptions import TaskNotFound


async def update_task(
    task_pk: int,
    task_data: TaskUpdateDTO,
    uow: ITaskUnitOfWork,
) -> Task:
    """
    Update an existing task.

    This function updates the task's details in the database and commits the transaction.

    :param task_id: ID of the task to update.
    :param updated_data: Data Transfer Object containing the updated task details.
    :param uow: Unit of Work instance for handling task repository operations.
    :return: The updated task object.
    """
    updated_task = TaskUpdate(
        id = task_pk,
        **{key: value for key, value in task_data.model_dump(mode="json").items() if value is not None}
    )

    async with uow:
        task = await uow.tasks.update(updated_task)
        await uow.commit()
    print(task.dict)
    return task
