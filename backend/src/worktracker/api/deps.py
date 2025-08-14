# backend/src/worktracker/api/deps.py
from __future__ import annotations

from typing import Annotated
from fastapi import Depends
from sqlmodel import Session

# --- DB Session provider ---
from ..core.db import get_session  # Session(engine) açan generator


def get_db(session: Session = Depends(get_session)) -> Session:
    """
    Her HTTP isteği için bir SQLModel Session üretir ve döndürür.
    Endpoint tamamlandığında (hata olsa bile) session kapanır.
    """
    return session


# --- WebSocket Hub provider (singleton benzeri) ---
from ..realtime.hub import WebSocketHub

_ws_hub_singleton: WebSocketHub | None = None


def get_ws_hub() -> WebSocketHub:
    global _ws_hub_singleton
    if _ws_hub_singleton is None:
        _ws_hub_singleton = WebSocketHub()
    return _ws_hub_singleton


# --- User: repository & service providers ---
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
    ws_hub: WebSocketHub = Depends(get_ws_hub),  # WS hub enjekte
) -> UserServicePort:
    """
    User servisini üretir (istek başına).
    WebSocket event'leri için hub enjekte edilir.
    """
    return UserService(repo, ws_publisher=ws_hub)


# --- Task: repository & service providers ---
from ..repositories.ports import TaskRepositoryPort
from ..repositories.sqlmodel_task_repo import SQLModelTaskRepository
from ..services.ports import TaskServicePort
from ..services.task_service import TaskService


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


__all__ = (
    "get_db",
    "get_ws_hub",
    "get_user_repository",
    "get_user_service",
    "get_task_repository",
    "get_task_service",
)
