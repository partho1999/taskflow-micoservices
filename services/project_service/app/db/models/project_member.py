import uuid
from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class ProjectMember(Base):
    __tablename__ = "project_members"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(String, nullable=False)
    role = Column(String, default="member")  # roles: owner, admin, member
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship back to Project
    project = relationship("Project", back_populates="members")
