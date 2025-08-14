from __future__ import annotations

from typing import Protocol, runtime_checkable
from worktracker.schemas.user import UserCreate, UserRead, UserUpdate


@runtime_checkable
class UserServicePort(Protocol):
    """
    API katmanının bağımlı olacağı servis arayüzü.
    Servis somut sınıfı (UserService) bu imzaları sağlar.
    """

    def create(self, data: UserCreate) -> UserRead: ...
    def get(self, user_id: int) -> UserRead: ...
    def update(self, user_id: int, data: UserUpdate) -> UserRead: ...
