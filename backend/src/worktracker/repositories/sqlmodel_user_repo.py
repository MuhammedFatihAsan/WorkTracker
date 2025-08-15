from __future__ import annotations

from typing import Optional
from sqlmodel import Session

from backend.src.worktracker.models.user import User
from backend.src.worktracker.repositories.ports import UserRepositoryPort

class SQLModelUserRepository(UserRepositoryPort):
    """
    User veri erişimi için SQLModel/PostgreSQL implementasyonu.
    - Sadece DB CRUD yapar.
    - commit/refresh ile kalıcı nesneyi döndürür.
    - Bulunamayan kayıtta update() ValueError atar (service 404'a çevirir).
    - UNIQUE ihlalinde (email) IntegrityError yukarı fırlar (service 409'a çevirir).
    """

    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, *, email: str, full_name: Optional[str] = None) -> User:
        user = User(email=email, full_name=full_name)
        self.session.add(user)
        self.session.commit()       # INSERT
        self.session.refresh(user)  # DB'nin son halini (id dahil) nesneye çeker
        return user

    def get_by_id(self, user_id: int) -> Optional[User]:
        return self.session.get(User, user_id)

    def update(
        self,
        user_id: int,
        *,
        email: Optional[str] = None,
        full_name: Optional[str] = None,
    ) -> User:
        user = self.session.get(User, user_id)
        if not user:
            # Service katmanı NotFoundError'a çevirir
            raise ValueError("User not found")

        if email is not None:
            user.email = email
        if full_name is not None:
            user.full_name = full_name

        self.session.add(user)
        self.session.commit()       # UPDATE
        self.session.refresh(user)
        return user
