from pydantic import BaseModel
from datetime import datetime
from typing import Any, Literal, Optional


class TaskDTO(BaseModel):
    """
    DTO representing a task for data transfer.

    Attributes:
        id (int): Unique identifier for the task.
        title (str): Title of the task.
        description (Optional[str]): Description of the task (optional field).
        status (Literal["pending", "completed", "archived"]): Status of the task.
        created_at (datetime): Date and time when the task was created.
        updated_at (datetime): Date and time when the task was last updated.
    """
    id: int
    title: str
    description: Optional[str] = None
    status: Literal["pending", "completed", "archived"]
    created_at: datetime
    updated_at: datetime
    owner_id: int


class TaskCreateDTO(BaseModel):
    """
    DTO representing the data for creating a new task.

    Attributes:
        title (str): Title of the new task (mandatory field).
        description (Optional[str]): Description of the new task (optional field).
    """
    title: str
    description: Optional[str] = None


class TaskUpdateDTO(BaseModel):
    """
    DTO representing the data for updating an existing task.

    Attributes:
        title (Optional[str]): New title for the task (optional field).
        description (Optional[str]): New description for the task (optional field).
        status (Optional[Literal["pending", "completed", "archived"]]): New status for the task (optional field).
    """
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[Literal["pending", "completed", "archived"]] = None
