from pathlib import Path
from fastapi import FastAPI
from .db.init_db import init_db
from .api.runs import router as runs_router

app = FastAPI(
    title="ML Experiment Tracker",
    version="0.1.0",
    description="Local-first experiment tracking API (mini W&B).",
)

@app.on_event("startup")
def on_startup() -> None:
    Path("data").mkdir(exist_ok=True)
    init_db()

app.include_router(runs_router)

@app.get("/health")
def health_check() -> dict:
    return {"status": "ok"}

@app.get("/")
def root() -> dict:
    return {
        "message": "ML Experiment Tracker API is running",
        "docs": "/docs",
        "health": "/health",
    }