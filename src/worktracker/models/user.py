from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

from worktracker.models.task import Task

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    # email'i hem indeksli hem benzersiz yapıyoruz
    email: str = Field(index=True, unique=True)
    full_name: Optional[str] = None

    # 1 kullanıcının birden çok task'ı olabilir
    tasks: List["Task"] = Relationship(back_populates="assignee")
