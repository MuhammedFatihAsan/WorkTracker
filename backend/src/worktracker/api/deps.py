from __future__ import annotations

from typing import Annotated
from fastapi import Depends
from sqlmodel import Session

from ..core.db import get_session  # Session(engine) açan generator

def get_db(session: Session = Depends(get_session)) -> Session:
    """
    Her HTTP isteği için bir SQLModel Session üretir ve döndürür.
    Endpoint tamamlandığında (hata olsa bile) session kapanır.
    """
    return session


# --- User tarafı: Repository & Service provider'ları ---

from ..repositories.ports import UserRepositoryPort
from ..repositories.sqlmodel_user_repo import SQLModelUserRepository
from ..services.ports import UserServicePort
from ..services.user_service import UserService

def get_user_repository(
    db: Annotated[Session, Depends(get_db)],
) -> UserRepositoryPort:
    """SQLModel tabanlı User repository'sini üretir (istek başına)."""
    return SQLModelUserRepository(db)

def get_user_service(
    repo: Annotated[UserRepositoryPort, Depends(get_user_repository)],
) -> UserServicePort:
    """
    User servisini üretir (istek başına).
    İleride WebSocket Hub enjekte etmek istersen:
      return UserService(repo, ws_publisher=ws_hub)
    """
    return UserService(repo)


__all__ = (
    "get_db",
    "get_user_repository",
    "get_user_service",
)
