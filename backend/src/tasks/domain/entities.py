from typing import Any, Literal, Optional
from dataclasses import dataclass
from datetime import datetime

from src.core.domain.entity_base import EntityBase


@dataclass
class Task(EntityBase):
    """
    Entity model representing a task in the task list.

    Attributes:
        id (int): Unique identifier for the task.
        title (str): Title of the task.
        description (Optional[str]): Description of the task (optional field).
        status (str): Status of the task. Can take the values:
                      "pending" (awaiting execution), 
                      "completed" (completed), 
                      "archived" (archived). 
                      Default is "pending".
        created_at (datetime): Date and time when the task was created. 
                               Default is the current time.
        updated_at (datetime): Date and time when the task was last updated. 
                               Default is the current time.
    """
    id: int
    title: str
    owner_id: int
    description: Optional[str] = None
    status: Literal["pending", "completed", "archived"] = "pending"
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()


@dataclass
class TaskCreate(EntityBase):
    """
    Entity model representing the data for creating a new task.

    Attributes:
        title (str): Title of the new task (mandatory field).
        description (Optional[str]): Description of the new task (optional field).
    """
    title: str
    owner_id: int
    description: Optional[str] = None


@dataclass
class TaskUpdate(EntityBase):
    """
    Entity model representing the data for updating an existing task.

    Attributes:
        title (Optional[str]): New title for the task (optional field).
        description (Optional[str]): New description for the task (optional field).
        status (Optional[str]): New status for the task. Can take the values:
                                "pending" (awaiting execution), 
                                "completed" (completed), 
                                "archived" (archived) (optional field).
    """
    id: int
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[Literal["pending", "completed", "archived"]] = None
