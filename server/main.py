from fastapi import FastAPI

app = FastAPI(
    title="ML Experiment Tracker",
    version="0.1.0",
    description="Local-first experiment tracking API (mini W&B).",
)

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