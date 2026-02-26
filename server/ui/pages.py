import json
from pathlib import Path
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from ..db.models import Metric, Param, Run
from ..db.session import get_db

BASE_DIR = Path(__file__).resolve().parents[1]
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

router = APIRouter(prefix="/ui", tags=["ui"])

@router.get("")
def ui_index(request: Request, db: Session = Depends(get_db)):
    runs: List[Run] = db.query(Run).order_by(Run.started_at.desc()).limit(50).all()
    return templates.TemplateResponse(
        "ui_index.html",
        {"request": request, "runs": runs},
    )

@router.get("/runs/{run_id}")
def ui_run_detail(run_id: int, request: Request, db: Session = Depends(get_db)):
    run = db.query(Run).filter(Run.id == run_id).first()
    if run is None:
        raise HTTPException(status_code=404, detail="Run not found")

    params = (
        db.query(Param)
        .filter(Param.run_id == run_id)
        .order_by(Param.key.asc())
        .all()
    )

    metric_names = [
        row[0]
        for row in db.query(Metric.name).filter(Metric.run_id == run_id).distinct().all()
    ]
    metric_names.sort()

    return templates.TemplateResponse(
        "ui_run_detail.html",
        {
            "request": request,
            "run": run,
            "params": params,
            "metric_names": metric_names,
            "metric_names_json": json.dumps(metric_names),
        },
    )