from fastapi import Depends
from sqlmodel import Session
from ..core.db import get_session  # get_session: core/db.py içinde engine'dan Session açan generator

def get_db(session: Session = Depends(get_session)) -> Session:
    """
    FastAPI dependency (bağımlılık) fonksiyonu.
    - Depends(get_session): Her HTTP isteği için get_session generator'ından bir Session üretir.
    - get_session, 'with Session(engine) as session: yield session' kalıbını kullanır.
      Bu sayede endpoint fonksiyonu bittiğinde (hata olsa bile) session otomatik kapanır.
    - Burada ekstra bir işlem yapmıyoruz; sadece alınan session'ı geri döndürüyoruz.
    """
    return session
