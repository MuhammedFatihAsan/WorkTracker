from logging.config import fileConfig
from alembic import context
from sqlalchemy import engine_from_config, pool

# ---------- BİZİM İMPORTLAR ----------
from sqlmodel import SQLModel
from src.worktracker.core.config import settings
from src.worktracker.models import *  # User, Task, TaskStatus (metadata için lazım)
# -------------------------------------

# Alembic Config nesnesi
config = context.config

# .ini dosyası varsa logging’i yükle
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# DB URL'i .env üzerinden dinamik ver
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# SQLModel metadata hedefi (autogenerate bunu kullanır)
target_metadata = SQLModel.metadata

def run_migrations_offline() -> None:
    """DB bağlantısı açmadan SQL script üretmek için."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,  # tip değişikliklerini de karşılaştır
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Gerçek bağlantı ile migration çalıştırmak için."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,  # tip değişikliklerini de karşılaştır
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
