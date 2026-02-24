from datetime import datetime
from typing import Any, Optional
from pydantic import BaseModel, ConfigDict, Field

class ParamItem(BaseModel):
    key: str = Field(min_length=1, max_length=200)
    value: Any

class ParamRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    run_id: int
    key: str
    value: str
    created_at: datetime

class MetricItem(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    value: float
    step: int = Field(ge=0, default=0)
    timestamp: Optional[datetime] = None

class MetricRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    run_id: int
    name: str
    value: float
    step: int
    timestamp: datetime