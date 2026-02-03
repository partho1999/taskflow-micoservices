import re
import uuid
from sqlalchemy import Column, String, DateTime, JSON, event
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

def generate_slug(name: str, org_id: str) -> str:
    slug_base = re.sub(r'[^a-zA-Z0-9\- ]', '', name).strip().lower().replace(' ', '-')
    return f"{slug_base}-{org_id[:6]}"

class Project(Base):
    __tablename__ = "projects"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    name = Column(String, nullable=False)
    slug = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)
    org_id = Column(String, index=True, nullable=False)
    owner_id = Column(String, nullable=False)
    extra = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship to ProjectMember
    members = relationship(
        "ProjectMember",
        back_populates="project",
        cascade="all, delete-orphan"
    )

@event.listens_for(Project, "before_insert")
def set_project_slug(mapper, connection, target: Project):
    if target.name and target.org_id:
        target.slug = generate_slug(target.name, target.org_id)
