# WorkTracker

**WorkTracker**, kullanıcı ve görev yönetimi için geliştirilmiş, **FastAPI + SQLModel + PostgreSQL** tabanlı bir REST API uygulamasıdır.
Docker Compose ile kolayca ayağa kalkar, `.env` üzerinden yapılandırılır. Alembic ile şema değişiklikleri versiyonlanır.

---

## 🚀 Özellikler

* **FastAPI** ile yüksek performanslı API
* **SQLModel** (Pydantic v2 + SQLAlchemy) veritabanı modelleri
* **Alembic** ile migration yönetimi (autogenerate + upgrade/downgrade)
* **PostgreSQL** (Docker Compose)
* **Ortam değişkenleri** ile yapılandırma
* **Katmanlı mimari**

  * **API**: Router’lar ve dependency’ler (HTTP ↔ domain çevirisi)
  * **Service**: İş kuralları (ör. `user_service`), domain hataları (`NotFoundError`, `ConflictError`)
  * **Models**: SQLModel modelleri (`User`, `Task`, `TaskStatus`)
  * **Schemas**: Request/Response şemaları (Create/Read/Update)
  * **Core**: Config & DB bağlantısı
  * **Alembic**: Migration’lar
* **Swagger UI**: `/docs`
* **Güncel validasyonlar**

  * `EmailStr` (email format kontrolü) — `email-validator` paketi gerekir
  * Pydantic v2: `Field(pattern=...)` kullanımı (eski `regex=` kaldırıldı)
  * `constr(strip_whitespace=True, min_length=...)` ile string kısıtları

> Not: Repository katmanı şimdilik boş/opsiyonel. İş kuralları **service** katmanında tutuluyor (şimdilik Users için uygulanmış durumda).

---

## 📂 Proje Yapısı

```
WorkTracker/
├─ .gitignore
├─ README.md
├─ requirements.txt
├─ docker-compose.yml
├─ .env
├─ .env.example
├─ alembic/
│  ├─ env.py
│  ├─ script.py.mako
│  └─ versions/           # migration dosyaları
└─ src/
   └─ worktracker/
      ├─ main.py          # FastAPI app
      ├─ api/
      │  ├─ deps.py       # DB session dependency
      │  └─ routers/
      │     ├─ __init__.py
      │     ├─ users.py
      │     └─ tasks.py
      ├─ services/
      │  ├─ __init__.py
      │  ├─ errors.py     # NotFoundError, ConflictError
      │  └─ user_service.py
      ├─ repositories/    # (opsiyonel/boş)
      ├─ models/
      │  ├─ __init__.py   # import sırası önemli (User -> Task)
      │  ├─ user.py
      │  └─ task.py
      ├─ schemas/
      │  ├─ __init__.py
      │  ├─ user.py
      │  └─ task.py
      └─ core/
         ├─ __init__.py
         ├─ config.py     # .env yükleme
         └─ db.py         # engine, get_session()
```

---

## ⚙️ Gereksinimler

* Python 3.11+
* Docker & Docker Compose
* (İsteğe bağlı) `psql` istemcisi

---

## 🛠️ Kurulum

### 1) Depoyu klonla

```bash
git clone https://github.com/MuhammedFatihAsan/worktracker.git
cd worktracker
```

### 2) Sanal ortam ve bağımlılıklar

```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
# venv\Scripts\activate    # Windows

pip install -r requirements.txt
```

> Eğer `EmailStr` kullanıyorsanız: `email-validator` paketi gereklidir (requirements’ta mevcut olmalı).

### 3) Ortam değişkenleri

`.env.example` dosyasını `.env` olarak kopyalayın ve düzenleyin:

```bash
cp .env.example .env
```

**`.env.example` örneği:**

```
DATABASE_URL=postgresql+psycopg2://worktracker:worktracker@localhost:5432/worktracker
```

### 4) PostgreSQL’i başlat (Docker)

```bash
docker-compose up -d
```

### 5) Migration uygula (ilk kez)

```bash
# Proje kökünde çalışın
export PYTHONPATH=$(pwd)               # Mac/Linux
# $env:PYTHONPATH=(Get-Location).Path  # Windows PowerShell

alembic upgrade head
```

### 6) API’yi çalıştır

```bash
uvicorn src.worktracker.main:app --reload
```

* Health check: [http://localhost:8000/health](http://localhost:8000/health)
* Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## ▶️ Hızlı Kullanım (cURL)

**User oluştur**

```bash
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{"email":"alice@example.com","full_name":"Alice"}'
```

**Task oluştur**

```bash
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"First Task","description":"demo","assignee_id":1}'
```

**Task listele**

```bash
curl http://localhost:8000/tasks
```

**Task güncelle**

```bash
curl -X PATCH http://localhost:8000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"status":"IN_PROGRESS"}'
```

---

## 🔒 Validasyon Kuralları (Özet)

* **UserCreate / UserUpdate**

  * `email: EmailStr` → e-posta formatı kontrolü (update’ta da geçerli)
  * `full_name: constr(strip_whitespace=True, min_length=1) | None` → boşluklar kırpılır, boş olamaz

* **TaskCreate**

  * `title: Field(pattern=r"^[A-Za-zÇĞİÖŞÜçğıöşü ]{2,50}$")`
  * `description: constr(strip_whitespace=True, min_length=1) | None`

* **TaskUpdate**

  * `title` **opsiyonel**; gelirse aynı pattern/uzunluk kuralları uygulanır
  * `description` **opsiyonel**; gelirse boş olamaz
  * `status: TaskStatus` (`TODO`, `IN_PROGRESS`, `DONE`)

---

## 🧩 Mimari Notlar

* **Service katmanı** (ör. `user_service.py`):

  * DB transaction, commit/rollback ve iş kuralları buradadır.
  * Domain hataları (`NotFoundError`, `ConflictError`) fırlatır; router bunları uygun HTTP kodlarına çevirir (404/409).
* **Router’lar**:

  * İnce tutulur; HTTP ↔ DTO ↔ service akışını yönetir.
  * ORM → DTO dönüşümü için `model_validate(obj, from_attributes=True)` kullanılır.
* **Alembic**:

  * `alembic/env.py` içinde:

    * `.env`’den URL: `config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)`
    * `target_metadata = SQLModel.metadata`
    * `compare_type=True`
    * `from src.worktracker.models import *` (metadata’yı doldurmak için)
  * `alembic/script.py.mako` içine **bir kez** `import sqlmodel` eklendi (AutoString için).

---

## ❗️ Sık Karşılaşılan Hatalar

* **`email-validator is not installed`**

  * Çözüm: `pip install email-validator` (veya `pip install "pydantic[email]")`
* **Pydantic v2: `regex` kaldırıldı**

  * Çözüm: `Field(pattern=...)` kullanın; projede buna göre güncellendi.
* **`ModuleNotFoundError: worktracker` (alembic/uvicorn)**

  * Kökte çalışın ve: `export PYTHONPATH=$(pwd)` (Mac/Linux)
  * Windows PowerShell: `$env:PYTHONPATH=(Get-Location).Path`
* **`NameError: sqlmodel is not defined` (migration)**

  * `alembic/script.py.mako` içine `import sqlmodel` ekleyin (bu repo’da eklendi).
* **Autogenerate fark görmüyor**

  * `env.py`’de `target_metadata=SQLModel.metadata` ve `from src.worktracker.models import *` olduğundan emin olun.
* **DB bağlantı hatası**

  * Docker Postgres up mı, port 5432 açık mı, `.env` URL doğru mu?

---

## 🧪 Test

```bash
pytest
```

---

## 📎 Lisans

Bu proje eğitim amaçlı hazırlanmıştır.

