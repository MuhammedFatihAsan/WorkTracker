from __future__ import annotations

from typing import Protocol, runtime_checkable, Optional
from worktracker.models import User

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
