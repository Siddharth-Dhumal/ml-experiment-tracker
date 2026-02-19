from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String
from .base import Base

class Run(Base):
    __tablename__ = "runs"

    id = Column(Integer, primary_key=True, index=True)
    project = Column(String, nullable=False, index=True)
    experiment = Column(String, nullable=False, index=True)
    name = Column(String, nullable=False)

    status = Column(String, nullable=False, default="running", index=True)
    started_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    ended_at = Column(DateTime, nullable=True)