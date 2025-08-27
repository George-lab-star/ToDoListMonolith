from fastapi import APIRouter, Depends

from src.users.domain.entities import User
from src.tasks.domain.dtos import TaskCreateDTO, TaskUpdateDTO, TaskDTO
from src.tasks.use_cases.task_create import create_task
from src.tasks.use_cases.task_read import read_task
from src.tasks.use_cases.task_update import update_task
from src.tasks.use_cases.task_delete import delete_task
from src.tasks.presentation.dependencies import TaskUoWDep
from src.users.presentation.dependencies import UserUoWDep
from src.auth.presentation.dependencies import AuthDep, get_current_user


task_api_router = APIRouter(prefix='/api/tasks', tags=["tasks"])


@task_api_router.post("", response_model=TaskDTO, status_code=201)
async def create(task_data: TaskCreateDTO, uow: TaskUoWDep, user_uow: UserUoWDep, user: AuthDep):
    """
    Create a new task.
    """
    return await create_task(owner_id=user.id, task_data=task_data, uow=uow, user_uow=user_uow)


@task_api_router.get("/{task_id}", response_model=TaskDTO)
async def get(task_id: int, uow: TaskUoWDep):
    """
    Get task by ID.
    """
    return await read_task(task_id, uow=uow)


@task_api_router.patch("/{task_id}", response_model=TaskDTO)
async def update(task_id: int, task_data: TaskUpdateDTO, uow: TaskUoWDep, user: AuthDep):
    """
    Update task data.
    """
    return await update_task(task_id, task_data, uow=uow)


@task_api_router.delete("/{task_id}", status_code=204)
async def delete(task_id: int, uow: TaskUoWDep, user: AuthDep):
    """
    Delete task by ID.
    """
    return await delete_task(task_id, uow=uow)
