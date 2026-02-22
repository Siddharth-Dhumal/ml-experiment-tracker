from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

class RunCreate(BaseModel):
    project: str = Field(min_length=1, max_length=100)
    experiment: str = Field(min_length=1, max_length=100)
    name: str = Field(min_length=1, max_length=200)

class RunRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    project: str
    experiment: str
    name: str
    status: str
    started_at: datetime
    ended_at: Optional[datetime] = None