# WorkTracker

**WorkTracker**, görev ve kullanıcı yönetimi için geliştirilmiş, **FastAPI** ve **PostgreSQL** tabanlı bir REST API uygulamasıdır.  
Docker Compose ile kolayca ayağa kaldırılabilir, `.env` dosyası üzerinden yapılandırılır ve modüler bir proje yapısına sahiptir.

---

## 🚀 Özellikler
- **FastAPI** ile yüksek performanslı API geliştirme
- **SQLModel** tabanlı veritabanı modelleri
- **Alembic** ile migration yönetimi
- **PostgreSQL** veritabanı (Docker Compose ile)
- Ortam değişkenleri ile kolay yapılandırma
- Katmanlı mimari:
  - API (routers, dependencies)
  - Service (iş mantığı)
  - Repository (veri erişim katmanı)
- Unit test altyapısı (pytest)

---

## 📂 Proje Yapısı
```
worktracker/
├─ .gitignore
├─ README.md
├─ requirements.txt
├─ docker-compose.yml
├─ Dockerfile
├─ .env
├─ .env.example
├─ alembic/                # Migration dosyaları
├─ tests/                  # Testler
└─ src/
   └─ worktracker/
      ├─ main.py           # FastAPI uygulama başlangıcı
      ├─ api/              # Endpoint tanımları
      ├─ services/         # İş mantığı
      ├─ repositories/     # Veri erişim katmanı
      ├─ models/           # SQLModel modelleri
      ├─ schemas/          # Pydantic şemaları
      └─ core/             # Konfigürasyon & DB bağlantısı
```

---

## 🛠️ Kurulum

### 1️⃣ Depoyu Klonla
```bash
git clone https://github.com/MuhammedFatihAsan/worktracker.git
cd worktracker
```

### 2️⃣ Sanal Ortam ve Bağımlılıklar
```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows

pip install -r requirements.txt
```

### 3️⃣ Ortam Değişkenleri
`.env.example` dosyasını `.env` olarak kopyalayın ve değerleri düzenleyin:
```bash
cp .env.example .env
```

### 4️⃣ Docker ile Veritabanını Başlat
```bash
docker compose up -d
```

### 5️⃣ API’yi Çalıştır
```bash
uvicorn src.worktracker.main:app --reload
```
[http://localhost:8000/health](http://localhost:8000/health) adresinden kontrol edebilirsiniz.

---

## 🧪 Test Çalıştırma
```bash
pytest
```

---

## 🔗 İlgili Kaynaklar
- [FastAPI Dokümantasyonu](https://fastapi.tiangolo.com/)
- [SQLModel](https://sqlmodel.tiangolo.com/)
- [Alembic](https://alembic.sqlalchemy.org/)
- [Docker Compose](https://docs.docker.com/compose/)
