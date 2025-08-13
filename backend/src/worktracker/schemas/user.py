from typing import Optional
from pydantic import EmailStr
from sqlmodel import SQLModel

class UserCreate(SQLModel):
    email: EmailStr # e-posta format doğrulaması
    full_name: Optional[str] = None

class UserRead(SQLModel):
    # İstemciye döneceğimiz alanlar (id dahil)
    id: int
    email: str
    full_name: Optional[str] = None

class UserUpdate(SQLModel):
    # PATCH için her alan opsiyonel (kısmi güncelleme)
    email: EmailStr | None = None
    full_name: Optional[str] = None
