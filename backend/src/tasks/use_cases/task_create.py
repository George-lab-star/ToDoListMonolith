from src.tasks.domain.entities import Task, TaskCreate
from src.tasks.domain.interfaces.task_uow import ITaskUnitOfWork
from src.tasks.domain.dtos import TaskCreateDTO
from src.users.domain.interfaces.user_uow import IUserUnitOfWork


async def create_task(
    owner_id: int,
    task_data: TaskCreateDTO,
    uow: ITaskUnitOfWork,
    user_uow: IUserUnitOfWork
) -> Task:
    """
    Create a new task in the system.

    This function creates a new task entity, saves it to the database, 
    and commits the transaction.

    :param task_data: Data Transfer Object containing task creation details.
    :param uow: Unit of Work instance for handling task repository operations.
    :return: Newly created task object.
    """
    new_task = TaskCreate(owner_id=owner_id, **task_data.model_dump())
    async with uow:
        created_task = await uow.tasks.add(new_task, user_uow)
        await uow.commit()
        return created_task
