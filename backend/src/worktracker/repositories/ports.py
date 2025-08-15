from __future__ import annotations
from typing import Protocol, runtime_checkable, Optional, List

from worktracker.models.task import Task, TaskStatus
from worktracker.models.user import User

@runtime_checkable
class UserRepositoryPort(Protocol):
    """User veri erişimi için repository arayüzü (sözleşme)."""

    def create(self, *, email: str, full_name: Optional[str] = None) -> User: ...
    def get_by_id(self, user_id: int) -> Optional[User]: ...
    def update(
        self,
        user_id: int,
        *,
        email: Optional[str] = None,
        full_name: Optional[str] = None,
    ) -> User: ...

@runtime_checkable
class TaskRepositoryPort(Protocol):
    """Task veri erişimi için repository arayüzü (sözleşme)."""

    def create(
        self,
        *,
        title: str,
        description: Optional[str] = None,
        status: TaskStatus = TaskStatus.TODO,
        assignee_id: Optional[int] = None,
    ) -> Task:
        """Yeni task oluştur ve persisted Task döndür."""
        ...

    def get_by_id(self, task_id: int) -> Optional[Task]:
        """ID ile task getir (yoksa None)."""
        ...

    def list(self) -> List[Task]:
        """Tüm task'leri getir (ileride filtre/paginasyon eklenebilir)."""
        ...

    def update(
        self,
        task_id: int,
        *,
        title: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[TaskStatus] = None,
        assignee_id: Optional[int] = None,
    ) -> Task:
        """Task'ı kısmi alanlarla güncelle ve persisted Task döndür."""
        ...
