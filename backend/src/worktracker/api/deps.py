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

# --- WebSocket Hub provider (singleton benzeri) ---
from ..realtime.hub import WebSocketHub
_ws_hub_singleton: WebSocketHub | None = None

def get_ws_hub() -> WebSocketHub:
    global _ws_hub_singleton
    if _ws_hub_singleton is None:
        _ws_hub_singleton = WebSocketHub()
    return _ws_hub_singleton


# --- Task providers ---
from typing import Annotated
from fastapi import Depends
from sqlmodel import Session

from ..repositories.ports import TaskRepositoryPort, UserRepositoryPort
from ..repositories.sqlmodel_task_repo import SQLModelTaskRepository
from ..services.ports import TaskServicePort
from ..services.task_service import TaskService
from .deps import get_db, get_user_repository  # eğer aynı dosyadaysa bu satırı kaldır

def get_task_repository(
    db: Annotated[Session, Depends(get_db)],
) -> TaskRepositoryPort:
    return SQLModelTaskRepository(db)

def get_task_service(
    task_repo: Annotated[TaskRepositoryPort, Depends(get_task_repository)],
    user_repo: Annotated[UserRepositoryPort, Depends(get_user_repository)],
    ws_hub: WebSocketHub = Depends(get_ws_hub),
) -> TaskServicePort:
    return TaskService(task_repo, user_repo, ws_publisher=ws_hub)
