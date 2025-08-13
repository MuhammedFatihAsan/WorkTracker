import os
from dotenv import load_dotenv

# .env dosyasını yükle (aynı klasörde veya proje kökünde arar)
load_dotenv()

class Settings:
    # .env'den DATABASE_URL oku; yoksa local hızlı denemeler için sqlite'a düş
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./worktracker.db")

# Uygulama genelinde import edip kullanacağımız tekil config nesnesi
settings = Settings()
