import json
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ..db.models import Metric, Param, Run
from ..db.session import get_db
from ..schemas.logging import MetricItem, MetricRead, ParamItem, ParamRead

router = APIRouter(prefix="/api/runs", tags=["logging"])

def _require_run(db: Session, run_id: int) -> Run:
    run = db.query(Run).filter(Run.id == run_id).first()
    if run is None:
        raise HTTPException(status_code=404, detail="Run not found")
    return run

@router.post("/{run_id}/params", response_model=List[ParamRead])
def upsert_params(
    run_id: int,
    items: List[ParamItem],
    db: Session = Depends(get_db),
) -> List[ParamRead]:
    _require_run(db, run_id)

    for item in items:
        key = item.key.strip()

        if isinstance(item.value, str):
            value_str = item.value
        else:
            value_str = json.dumps(item.value, separators=(",", ":"), ensure_ascii=False)

        existing = (
            db.query(Param)
            .filter(Param.run_id == run_id)
            .filter(Param.key == key)
            .first()
        )

        if existing:
            existing.value = value_str
        else:
            db.add(
                Param(
                    run_id=run_id,
                    key=key,
                    value=value_str,
                    created_at=datetime.utcnow(),
                )
            )

    db.commit()

    params = (
        db.query(Param)
        .filter(Param.run_id == run_id)
        .order_by(Param.key.asc())
        .all()
    )
    return [ParamRead.model_validate(p) for p in params]

@router.get("/{run_id}/params", response_model=List[ParamRead])
def list_params(run_id: int, db: Session = Depends(get_db)) -> List[ParamRead]:
    _require_run(db, run_id)

    params = (
        db.query(Param)
        .filter(Param.run_id == run_id)
        .order_by(Param.key.asc())
        .all()
    )
    return [ParamRead.model_validate(p) for p in params]

@router.post("/{run_id}/metrics", response_model=dict)
def log_metrics(
    run_id: int,
    items: List[MetricItem],
    db: Session = Depends(get_db),
) -> dict:
    _require_run(db, run_id)

    rows = []
    now = datetime.utcnow()

    for item in items:
        rows.append(
            Metric(
                run_id=run_id,
                name=item.name.strip(),
                value=float(item.value),
                step=int(item.step),
                timestamp=item.timestamp or now,
            )
        )

    db.add_all(rows)
    db.commit()

    return {"inserted": len(rows)}

@router.get("/{run_id}/metrics", response_model=List[MetricRead])
def list_metrics(
    run_id: int,
    name: Optional[str] = Query(default=None),
    limit: int = Query(default=500, ge=1, le=5000),
    db: Session = Depends(get_db),
) -> List[MetricRead]:
    _require_run(db, run_id)

    query = db.query(Metric).filter(Metric.run_id == run_id)
    if name:
        query = query.filter(Metric.name == name)

    metrics = query.order_by(Metric.step.asc(), Metric.timestamp.asc()).limit(limit).all()
    return [MetricRead.model_validate(m) for m in metrics]