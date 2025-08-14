from __future__ import annotations

from fastapi import FastAPI
from .api.routers import users, tasks, ws

#FastAPI uygulamasını başlat
app = FastAPI(title="WorkTracker")

# REST
app.include_router(users.router)
app.include_router(tasks.router)

# WebSocket
app.include_router(ws.router)

@app.get("/health")
def health():
    return {"status": "ok"}