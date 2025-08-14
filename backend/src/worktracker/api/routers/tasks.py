from __future__ import annotations

from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException

from ...schemas.task import TaskCreate, TaskUpdate, TaskRead
from ...services.ports import TaskServicePort
from ..deps import get_task_service
from ...services.task_service import NotFoundError, AssigneeNotFoundError

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("", response_model=TaskRead, status_code=201)
def create_task(
    data: TaskCreate,
    svc: Annotated[TaskServicePort, Depends(get_task_service)],
):
    try:
        return svc.create(data)
    except AssigneeNotFoundError:
        # Geçersiz assignee_id (kullanıcı yok / FK ihlali)
        raise HTTPException(status_code=400, detail="Assignee user not found")
    except Exception as ex:
        # Beklenmeyen/iş kuralı ihlalleri vs.
        raise HTTPException(status_code=400, detail=str(ex))

@router.get("/{task_id}", response_model=TaskRead)
def get_task(
    task_id: int,
    svc: Annotated[TaskServicePort, Depends(get_task_service)],
):
    try:
        return svc.get(task_id)
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Task not found")

@router.get("", response_model=list[TaskRead])
def list_tasks(
    svc: Annotated[TaskServicePort, Depends(get_task_service)],
):
    return svc.list()

@router.patch("/{task_id}", response_model=TaskRead)
def update_task(
    task_id: int,
    data: TaskUpdate,
    svc: Annotated[TaskServicePort, Depends(get_task_service)],
):
    try:
        return svc.update(task_id, data)
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Task not found")
    except AssigneeNotFoundError:
        raise HTTPException(status_code=400, detail="Assignee user not found")
