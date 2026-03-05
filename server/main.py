from pathlib import Path
from fastapi import FastAPI
from .db.init_db import init_db
from .api.runs import router as runs_router
from .api.logging import router as logging_router
from fastapi.staticfiles import StaticFiles
from .ui.pages import router as ui_router

app = FastAPI(
    title="ML Experiment Tracker",
    version="0.1.0",
    description="Local-first experiment tracking API (mini W&B).",
)

BASE_DIR = Path(__file__).resolve().parent
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
app.include_router(ui_router)

@app.on_event("startup")
def on_startup() -> None:
    Path("data").mkdir(exist_ok=True)
    init_db()

app.include_router(runs_router)
app.include_router(logging_router)

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