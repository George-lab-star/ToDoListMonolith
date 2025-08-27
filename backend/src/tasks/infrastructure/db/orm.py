from typing import Any, Optional
import datetime
import enum

from sqlalchemy import Integer, String, Text, DateTime, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base


class TaskStatus(enum.Enum):
    pending = "pending"
    completed = "completed"
    archived = "archived"


class DBTask(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[TaskStatus] = mapped_column(Enum(TaskStatus), default=TaskStatus.pending)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None))
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None), onupdate=lambda: datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None))
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id')) 
    owner: Mapped[Any] = relationship("DBUser", back_populates="tasks")
