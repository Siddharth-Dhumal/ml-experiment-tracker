from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ..db.models import Run
from ..db.session import get_db
from ..schemas.runs import RunCreate, RunRead

router = APIRouter(prefix="/api/runs", tags=["runs"])

@router.post("", response_model=RunRead, status_code=201)
def create_run(payload: RunCreate, db: Session = Depends(get_db)) -> RunRead:
    run = Run(
        project=payload.project.strip(),
        experiment=payload.experiment.strip(),
        name=payload.name.strip(),
        status="running",
    )
    db.add(run)
    db.commit()
    db.refresh(run)
    return RunRead.model_validate(run)

@router.get("", response_model=List[RunRead])
def list_runs(
    status: Optional[str] = Query(default=None),
    db: Session = Depends(get_db),
) -> List[RunRead]:
    query = db.query(Run)
    if status:
        query = query.filter(Run.status == status)

    runs = query.order_by(Run.started_at.desc()).all()
    return [RunRead.model_validate(r) for r in runs]

@router.get("/{run_id}", response_model=RunRead)
def get_run(run_id: int, db: Session = Depends(get_db)) -> RunRead:
    run = db.query(Run).filter(Run.id == run_id).first()
    if run is None:
        raise HTTPException(status_code=404, detail="Run not found")
    return RunRead.model_validate(run)