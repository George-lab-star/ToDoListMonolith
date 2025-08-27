from src.tasks.domain.interfaces.task_uow import ITaskUnitOfWork


async def delete_task(
    task_id: int,
    uow: ITaskUnitOfWork,
) -> None:
    """
    Delete a task by its ID.

    This function removes the task from the database and commits the transaction.

    :param task_id: ID of the task to delete.
    :param uow: Unit of Work instance for handling task repository operations.
    """
    async with uow:
        await uow.tasks.delete(task_id)
        await uow.commit()
