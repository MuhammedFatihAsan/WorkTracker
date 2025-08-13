from fastapi import FastAPI
from .api.routers import users_router, tasks_router

#FastAPI uygulamasını başlat
app = FastAPI(title="WorkTracker")

#HealthPoint
@app.get("/health")
def health_check():
    return {"status": "ok"}

# ÖNEMLİ: Router'ları uygulamaya ekle
# /users ile başlayan uçlar için users_router
app.include_router(users_router)
# /tasks ile başlayan uçlar için tasks_router
app.include_router(tasks_router)