import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Enum, Boolean, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base import Base
import enum

# Status Enum
class SubtaskStatus(str, enum.Enum):
    todo = "todo"
    in_progress = "in_progress"
    review = "review"
    done = "done"

# Priority Enum
class SubtaskPriority(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"
    urgent = "urgent"

class Subtask(Base):
    __tablename__ = "subtasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    task_id = Column(UUID(as_uuid=True), ForeignKey("tasks.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(String, nullable=True)
    priority = Column(Enum(SubtaskPriority), default=SubtaskPriority.medium)
    status = Column(Enum(SubtaskStatus), default=SubtaskStatus.todo)
    assignee_id = Column(UUID(as_uuid=True), nullable=True)
    reporter_id = Column(UUID(as_uuid=True), nullable=False)
    due_date = Column(DateTime, nullable=True)
    position = Column(Integer, default=0)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    task = relationship("Task", backref="subtasks")
