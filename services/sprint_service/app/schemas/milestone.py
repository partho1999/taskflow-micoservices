# app/schemas/milestone.py
from pydantic import BaseModel
from uuid import UUID
from datetime import date


class MilestoneCreate(BaseModel):
    title: str
    description: str | None = None
    due_date: date | None = None


class MilestoneUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    due_date: date | None = None
    status: str | None = None


class MilestoneOut(BaseModel):
    id: UUID
    sprint_id: UUID
    title: str
    description: str | None
    due_date: date | None
    status: str

    class Config:
        from_attributes = True
