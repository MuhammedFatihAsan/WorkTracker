from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from ...models import User                      # ORM modelimiz (SQLModel, table=True)
from ...schemas.user import UserCreate, UserRead, UserUpdate  # DTO/şema sınıfları
from ..deps import get_db                       # Session enjekte eden dependency

# Bu router, /users ile başlayan tüm endpoint'leri kapsar.
# 'tags' Swagger UI'da gruplama için kullanılır.
router = APIRouter(prefix="/users", tags=["users"])

@router.post("", response_model=UserRead, status_code=201)
def create_user(data: UserCreate, db: Session = Depends(get_db)):
    """
    Yeni kullanıcı oluşturur.
    - data: UserCreate şeması (POST body) → FastAPI/Pydantic otomatik doğrular.
    - db: Depends(get_db) sayesinde bu isteğe özel açılan Session.
    - İş akışı:
      1) ORM nesnesi oluştur (User)
      2) db.add → 'pending' hale gelir
      3) db.commit → INSERT'i işler, ID'yi DB üretir
      4) db.refresh → DB'deki son halini (id dahil) Python nesnesine çeker
      5) model_validate(..., from_attributes=True) → ORM objesini UserRead DTO'suna çevir
    """
    user = User(email=data.email, full_name=data.full_name)
    db.add(user)
    db.commit()
    db.refresh(user)
    return UserRead.model_validate(user, from_attributes=True)

@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    ID'ye göre tek kullanıcı getirir.
    - db.get(User, user_id) → Primary key üzerinden hızlı sorgu.
    - Bulunamazsa 404 fırlatılır.
    """
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(404, "User not found")
    return UserRead.model_validate(user, from_attributes=True)

@router.patch("/{user_id}", response_model=UserRead)
def update_user(user_id: int, data: UserUpdate, db: Session = Depends(get_db)):
    """
    Kısmi güncelleme (PATCH).
    - UserUpdate'teki tüm alanlar opsiyonel olduğundan gelen alanları tek tek kontrol ederiz.
    - Değişiklik yapıldıktan sonra commit + refresh.
    """
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(404, "User not found")

    # Sadece gönderilen alanları güncelle
    if data.email is not None:
        user.email = data.email
    if data.full_name is not None:
        user.full_name = data.full_name

    db.add(user)     # SQLAlchemy değişiklikleri takip eder; add güvenlidir (upsert gibi düşünmeyelim, var olan objeyi dirty olarak işaretler)
    db.commit()      # UPDATE işlemi
    db.refresh(user) # Güncel satırı tekrar yükle
    return UserRead.model_validate(user, from_attributes=True)
