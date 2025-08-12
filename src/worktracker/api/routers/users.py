from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from ...models import User
from ...schemas.user import UserCreate, UserRead, UserUpdate
from ..deps import get_db

router = APIRouter(prefix="/users", tags=["users"])

@router.post("", response_model=UserRead, status_code=201)
def create_user(data: UserCreate, db: Session = Depends(get_db)):
    # Basit create (aynı email tekrarında DB unique constraint patlatır)
    user = User(email=data.email, full_name=data.full_name)
    db.add(user)
    db.commit()
    db.refresh(user)
    return UserRead.model_validate(user, from_attributes=True)

@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(404, "User not found")
    return UserRead.model_validate(user, from_attributes=True)

@router.patch("/{user_id}", response_model=UserRead)
def update_user(user_id: int, data: UserUpdate, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(404, "User not found")

    if data.email is not None:
        user.email = data.email
    if data.full_name is not None:
        user.full_name = data.full_name

    db.add(user)
    db.commit()
    db.refresh(user)
    return UserRead.model_validate(user, from_attributes=True)
