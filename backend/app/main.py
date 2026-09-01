# FASTAPI config
from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(
    title="DevLens API",
    description="Codebase health and analysis API for DevLens",
    version="0.1.0",
)

app.include_router(router, prefix="/api/v1")

@app.get("/health")
def health_check():
    return {
        "status" : "ok",
        "service" : "DevLens API",
    }