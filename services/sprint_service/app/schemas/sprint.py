from datetime import datetime
from uuid import UUID
from pydantic import BaseModel
from typing import Optional
from app.models.sprint import SprintStatus


class SprintBase(BaseModel):
    name: str
    goal: Optional[str] = None
    start_date: datetime
    end_date: datetime
    status: Optional[SprintStatus] = SprintStatus.planned


class SprintCreate(SprintBase):
    pass  # All fields required from Base


class SprintUpdate(BaseModel):
    name: Optional[str]
    goal: Optional[str]
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    status: Optional[SprintStatus]


class SprintRead(SprintBase):
    id: UUID
    created_by: UUID
    created_at: datetime

    class Config:
        orm_mode = True
