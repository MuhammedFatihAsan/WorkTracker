from typing import TYPE_CHECKING, Optional, List
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .task import Task  # sadece tip kontrolünde import, runtime'da değil

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    # email'i hem indeksli hem benzersiz yapıyoruz
    email: str = Field(index=True, unique=True)
    full_name: Optional[str] = None

    # 1 kullanıcının birden çok task'ı olabilir
    tasks: List["Task"] = Relationship(back_populates="assignee")
