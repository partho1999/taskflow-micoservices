# app/models/milestone.py
import uuid
from sqlalchemy import Column, String, Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base import Base


class Milestone(Base):
    __tablename__ = "milestones"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sprint_id = Column(UUID(as_uuid=True), ForeignKey("sprints.id"), nullable=False)

    title = Column(String, nullable=False)
    description = Column(String)
    due_date = Column(Date)
    status = Column(String, default="pending")

    sprint = relationship("Sprint", back_populates="milestones")
