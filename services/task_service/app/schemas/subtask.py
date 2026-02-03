from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
import enum
import uuid

class SubtaskStatus(str, enum.Enum):
    todo = "todo"
    in_progress = "in_progress"
    review = "review"
    done = "done"

class SubtaskPriority(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"
    urgent = "urgent"

class SubtaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    priority: Optional[SubtaskPriority] = SubtaskPriority.medium
    status: Optional[SubtaskStatus] = SubtaskStatus.todo
    assignee_id: Optional[uuid.UUID] = None
    reporter_id: uuid.UUID
    due_date: Optional[datetime] = None

class SubtaskCreate(SubtaskBase):
    task_id: uuid.UUID

class SubtaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[SubtaskPriority] = None
    status: Optional[SubtaskStatus] = None
    assignee_id: Optional[uuid.UUID] = None
    due_date: Optional[datetime] = None

class SubtaskRead(SubtaskBase):
    id: uuid.UUID
    task_id: uuid.UUID
    position: int
    is_deleted: bool
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True  # <-- v2 way
    }
