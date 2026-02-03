from sqlalchemy.orm import Session
from uuid import UUID
from typing import List, Optional
from app.models.sprint import Sprint
from app.schemas.sprint import SprintCreate, SprintUpdate


class SprintService:
    def __init__(self, db: Session):
        self.db = db

    def create_sprint(self, sprint_in: SprintCreate, user_id: UUID) -> Sprint:
        sprint = Sprint(**sprint_in.dict(), created_by=user_id)
        self.db.add(sprint)
        self.db.commit()
        self.db.refresh(sprint)
        return sprint

    def get_sprint(self, sprint_id: UUID) -> Optional[Sprint]:
        return self.db.query(Sprint).filter(Sprint.id == sprint_id).first()

    def get_sprints(self, skip: int = 0, limit: int = 100) -> List[Sprint]:
        return self.db.query(Sprint).offset(skip).limit(limit).all()

    def update_sprint(self, sprint_id: UUID, sprint_in: SprintUpdate) -> Optional[Sprint]:
        sprint = self.get_sprint(sprint_id)
        if not sprint:
            return None
        for field, value in sprint_in.dict(exclude_unset=True).items():
            setattr(sprint, field, value)
        self.db.commit()
        self.db.refresh(sprint)
        return sprint

    def delete_sprint(self, sprint_id: UUID) -> bool:
        sprint = self.get_sprint(sprint_id)
        if not sprint:
            return False
        self.db.delete(sprint)
        self.db.commit()
        return True
