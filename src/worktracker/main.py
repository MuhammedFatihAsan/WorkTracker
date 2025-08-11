from fastapi import FastAPI

#FastAPI uygulamasını başlat
app = FastAPI(title="WorkTracker")

#HealthPoint
@app.get("/health")
def health_check():
    return {"status": "ok"} 