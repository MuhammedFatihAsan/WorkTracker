# src/worktracker/core/db.py
from sqlmodel import SQLModel, create_engine, Session
from .config import settings

# Engine: veritabanına bağlantıyı ve havuzu yönetir
# settings.DATABASE_URL ör: postgresql+psycopg2://worktracker:worktracker@localhost:5432/worktracker
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)

def get_session():
    """
    FastAPI dependency olarak kullanılacak generator.
    'yield' ile dışarı bir Session verir, fonksiyon dönerken (scope bitince)
    context çıkışında session kapanır.
    """
    with Session(engine) as session:
        yield session

def init_db():
    """
    Hızlı local denemelerde tablo şemasını koddan yaratmak istersen:
    SQLModel.metadata.create_all(engine)
    Biz migration için Alembic kullanacağımızdan burada pas geçiyoruz.
    """
    pass
