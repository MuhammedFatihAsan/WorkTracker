from __future__ import annotations

from typing import Protocol, runtime_checkable, List

from backend.src.worktracker.schemas.task import TaskCreate, TaskRead, TaskUpdate
from backend.src.worktracker.schemas.user import UserCreate, UserRead, UserUpdate


@runtime_checkable
class UserServicePort(Protocol):
    """
    API katmanının bağımlı olacağı servis arayüzü.
    Servis somut sınıfı (UserService) bu imzaları sağlar.
    """

    def create(self, data: UserCreate) -> UserRead: ...
    def get(self, user_id: int) -> UserRead: ...
    def update(self, user_id: int, data: UserUpdate) -> UserRead: ...

@runtime_checkable
class TaskServicePort(Protocol):
    """
    Task tarafı servis sözleşmesi.
    - Servis; iş kurallarını uygular (örn. assignee_id verildiyse kullanıcı var mı kontrolü),
      repository'yi çağırır, ORM -> DTO dönüşümü yapar ve gerekirse WS event publish eder.
    """

    def create(self, data: TaskCreate) -> TaskRead: ...
    def get(self, task_id: int) -> TaskRead: ...
    def list(self) -> List[TaskRead]: ...
    def update(self, task_id: int, data: TaskUpdate) -> TaskRead: ...