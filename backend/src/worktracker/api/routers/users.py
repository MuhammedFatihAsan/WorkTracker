from __future__ import annotations

from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException

from ...schemas.user import UserCreate, UserRead, UserUpdate
from ...services.ports import UserServicePort
from ..deps import get_user_service
from ...services.user_service import NotFoundError, DuplicateEmailError

router = APIRouter(prefix="/users", tags=["users"])

@router.post("", response_model=UserRead, status_code=201)
def create_user(
    data: UserCreate,
    svc: Annotated[UserServicePort, Depends(get_user_service)],
):
    try:
        return svc.create(data)
    except DuplicateEmailError:
        # email UNIQUE ihlali
        raise HTTPException(status_code=409, detail="Email already exists")
    except Exception as ex:
        # beklenmeyen/iş kuralı ihlalleri vs.
        raise HTTPException(status_code=400, detail=str(ex))

@router.get("/{user_id}", response_model=UserRead)
def get_user(
    user_id: int,
    svc: Annotated[UserServicePort, Depends(get_user_service)],
):
    try:
        return svc.get(user_id)
    except NotFoundError:
        raise HTTPException(status_code=404, detail="User not found")

@router.patch("/{user_id}", response_model=UserRead)
def update_user(
    user_id: int,
    data: UserUpdate,
    svc: Annotated[UserServicePort, Depends(get_user_service)],
):
    try:
        return svc.update(user_id, data)
    except NotFoundError:
        raise HTTPException(status_code=404, detail="User not found")
    except DuplicateEmailError:
        raise HTTPException(status_code=409, detail="Email already exists")
