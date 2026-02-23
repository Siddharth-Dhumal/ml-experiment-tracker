from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String
from .base import Base
import json
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, UniqueConstraint

class Run(Base):
    __tablename__ = "runs"

    id = Column(Integer, primary_key=True, index=True)
    project = Column(String, nullable=False, index=True)
    experiment = Column(String, nullable=False, index=True)
    name = Column(String, nullable=False)

    status = Column(String, nullable=False, default="running", index=True)
    started_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    ended_at = Column(DateTime, nullable=True)

class Param(Base):
    __tablename__ = "params"

    id = Column(Integer, primary_key=True, index=True)
    run_id = Column(Integer, ForeignKey("runs.id"), nullable=False, index=True)

    key = Column(String, nullable=False)
    value = Column(String, nullable=False)

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("run_id", "key", name="uq_params_run_id_key"),
    )


class Metric(Base):
    __tablename__ = "metrics"

    id = Column(Integer, primary_key=True, index=True)
    run_id = Column(Integer, ForeignKey("runs.id"), nullable=False, index=True)

    name = Column(String, nullable=False, index=True)
    step = Column(Integer, nullable=False, default=0)
    value = Column(Float, nullable=False)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)