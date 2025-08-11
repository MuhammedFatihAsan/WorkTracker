from typing import Optional
from enum import Enum
from sqlmodel import SQLModel, Field, Relationship

from worktracker.models.user import User

class TaskStatus(str, Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"

class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None
    status: TaskStatus = Field(default=TaskStatus.TODO)

    # Many-to-One: bir task bir kullanıcıya atanabilir
    assignee_id: Optional[int] = Field(default=None, foreign_key="users.id")
    assignee: Optional["User"] = Relationship(back_populates="tasks")
