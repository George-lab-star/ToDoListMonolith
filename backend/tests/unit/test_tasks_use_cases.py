from unittest.mock import MagicMock
import pytest

from src.tasks.use_cases.task_create import create_task
from src.tasks.use_cases.task_read import read_task
from src.tasks.use_cases.task_update import update_task
from src.tasks.use_cases.task_delete import delete_task
from src.tasks.domain.dtos import TaskCreateDTO, TaskUpdateDTO
from src.tasks.domain.entities import Task
from src.tasks.domain.exceptions import TaskNotFound
from src.tasks.domain.interfaces.task_uow import ITaskUnitOfWork
from src.users.domain.interfaces.user_uow import IUserUnitOfWork


task_create_dto = TaskCreateDTO(
    title="Test Task",
    description="This is a test task.",
)


@pytest.mark.asyncio
async def test_create_task(fake_task_uow: ITaskUnitOfWork, fake_user_uow: IUserUnitOfWork):
    """
    Test that a task can be successfully created.
    """
    task = await create_task(owner_id=1, task_data=task_create_dto, uow=fake_task_uow, user_uow=fake_user_uow)
    assert task.title == task_create_dto.title
    assert task.description == task_create_dto.description


@pytest.mark.asyncio
async def test_get_task(fake_task_uow: ITaskUnitOfWork, fake_user_uow: IUserUnitOfWork):
    """
    Test retrieving a task by ID.

    Verifies that a created task is returned correctly,
    and that requesting a non-existent task raises TaskNotFound.
    """
    task = await _create_task(fake_task_uow, fake_user_uow)
    result = await read_task(task_pk=task.id, uow=fake_task_uow)
    assert result.id == task.id
    assert result.title == task_create_dto.title

    with pytest.raises(TaskNotFound) as exc:
        await read_task(task_pk=-1, uow=fake_task_uow)
    assert exc.type is TaskNotFound


@pytest.mark.asyncio
async def test_update_task(fake_task_uow: ITaskUnitOfWork, fake_user_uow: IUserUnitOfWork):
    """
    Test updating a task's title.

    Verifies that the title is updated correctly, and that updating
    a non-existent task raises TaskNotFound.
    """
    task = await _create_task(fake_task_uow, fake_user_uow)

    update_data = TaskUpdateDTO(title="Updated Test Task")
    updated_task = await update_task(task_pk=task.id, task_data=update_data, uow=fake_task_uow)
    assert updated_task.id == task.id
    assert updated_task.title == update_data.title

    with pytest.raises(TaskNotFound) as exc:
        await update_task(task_pk=-1, task_data=update_data, uow=fake_task_uow)
    assert exc.type is TaskNotFound


@pytest.mark.asyncio
async def test_delete_task(fake_task_uow: ITaskUnitOfWork, fake_user_uow: IUserUnitOfWork):
    """
    Test deleting a task by ID.

    Ensures that deletion returns None and that deleting
    the same task again raises TaskNotFound.
    """
    task = await _create_task(fake_task_uow, fake_user_uow)
    result = await delete_task(task_id=task.id, uow=fake_task_uow)
    assert result is None

    with pytest.raises(TaskNotFound) as exc:
        await delete_task(task_id=task.id, uow=fake_task_uow)
    assert exc.type is TaskNotFound


async def _create_task(task_uow: ITaskUnitOfWork, fake_user_uow: IUserUnitOfWork) -> Task:
    """
    Helper function to create a task using a mocked unit of work.

    :param task_uow: Fake unit of work.
    :return: Created Task entity.
    """
    task = await create_task(owner_id=1, task_data=task_create_dto, uow=task_uow, user_uow=fake_user_uow)
    assert task.title == task_create_dto.title
    assert task.description == task_create_dto.description
    return task
