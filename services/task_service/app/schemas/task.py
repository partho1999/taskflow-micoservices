from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from datetime import datetime
from app.models.task import TaskStatus, TaskPriority

# -----------------------------
# Base Task Schema
# -----------------------------
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    priority: Optional[TaskPriority] = TaskPriority.medium
    status: Optional[TaskStatus] = TaskStatus.todo
    assignee_id: Optional[UUID] = None
    due_date: Optional[datetime] = None

# -----------------------------
# Schema for Task Creation
# -----------------------------
class TaskCreate(TaskBase):
    project_id: Optional[UUID] = None   # will be filled from URL
    reporter_id: Optional[UUID] = None  # will be filled from JWT

# -----------------------------
# Schema for Task Update
# -----------------------------
class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[TaskPriority] = None
    status: Optional[TaskStatus] = None
    assignee_id: Optional[UUID] = None
    due_date: Optional[datetime] = None

# -----------------------------
# Schema for Task Output
# -----------------------------
class TaskOut(TaskBase):
    id: UUID
    project_id: UUID
    reporter_id: UUID
    sprint_id: UUID
    position: int
    created_at: datetime
    updated_at: datetime

    # ✅ Pydantic v2 change: orm_mode -> from_attributes
    model_config = {
        "from_attributes": True
    }

class AssignSprintToTasks(BaseModel):
    sprint_id: UUID
    task_ids: List[UUID]