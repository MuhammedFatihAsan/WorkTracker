from __future__ import annotations

from typing import Optional, Any
from sqlalchemy.exc import IntegrityError

from worktracker.repositories.ports import UserRepositoryPort
from worktracker.schemas.user import UserCreate, UserRead, UserUpdate

class NotFoundError(Exception):
    """Kaynak bulunamadığında servis katmanının fırlattığı domain hatası."""
    pass


class DuplicateEmailError(Exception):
    """Email UNIQUE kısıtı ihlal edildiğinde servis katmanında yükseltilir."""
    pass


class UserService:
    """
    User iş kuralları + mapping.
    Gerektiğinde WebSocket publisher enjekte edilebilir (ws_publisher).
    """

    def __init__(
        self,
        user_repo: UserRepositoryPort,
        *,
        ws_publisher: Optional[Any] = None,  # ileride publish için
    ) -> None:
        self.user_repo = user_repo
        self.ws = ws_publisher

    # --- Normalizasyon yardımcıları ---
    def _norm_email(self, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        s = v.strip().lower()
        return s or None  # boş string geldiyse None yap

    def _norm_name(self, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        s = v.strip()
        return s or None

    # --- İşlevler ---
    def create(self, data: UserCreate) -> UserRead:
        # Pydantic EmailStr -> str çevirip normalize et
        email = self._norm_email(str(data.email))
        full_name = self._norm_name(data.full_name)

        try:
            user = self.user_repo.create(email=email, full_name=full_name)
        except IntegrityError as e:
            # Genelde UNIQUE ihlali (email). İstersen e.orig.pgcode ile 23505 kontrolü yapabilirsin.
            raise DuplicateEmailError("Email already exists") from e

        # WS publish (başarılı create sonrası)
        if self.ws:
            try:
                self.ws.publish_user_created(user.id)
            except Exception:
                pass

        return UserRead.model_validate(user, from_attributes=True)

    def get(self, user_id: int) -> UserRead:
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundError("User not found")
        return UserRead.model_validate(user, from_attributes=True)

    def update(self, user_id: int, data: UserUpdate) -> UserRead:
        email = self._norm_email(str(data.email)) if data.email is not None else None
        full_name = self._norm_name(data.full_name) if data.full_name is not None else None

        try:
            user = self.user_repo.update(
                user_id,
                email=email,
                full_name=full_name,
            )
        except ValueError:
            # Repo "bulunamadı"yı ValueError ile bildiriyor → serviste domain hatasına çevir
            raise NotFoundError("User not found")
        except IntegrityError as e:
            raise DuplicateEmailError("Email already exists") from e

        # WS publish (başarılı update sonrası)
        if self.ws:
            try:
                self.ws.publish_user_updated(user.id)
            except Exception:
                pass

        return UserRead.model_validate(user, from_attributes=True)
