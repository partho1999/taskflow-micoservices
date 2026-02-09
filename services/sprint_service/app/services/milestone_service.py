# app/services/milestone_service.py
import uuid
from sqlalchemy.orm import Session
from app.models.milestone import Milestone


class MilestoneService:
    def __init__(self, db: Session):
        self.db = db

    def create_milestone(self, sprint_id, data):
        milestone = Milestone(
            id=uuid.uuid4(),
            sprint_id=sprint_id,
            **data.dict()
        )
        self.db.add(milestone)
        self.db.commit()
        self.db.refresh(milestone)
        return milestone

    def get_sprint_milestones(self, sprint_id):
        return self.db.query(Milestone).filter_by(sprint_id=sprint_id).all()
    
    def get_milestone(self, milestone_id):
        milestone = self.db.query(Milestone).get(milestone_id)
        return milestone

    def update_milestone(self, milestone_id, data):
        milestone = self.db.query(Milestone).get(milestone_id)
        if not milestone:
            return None

        for key, value in data.dict(exclude_unset=True).items():
            setattr(milestone, key, value)

        self.db.commit()
        self.db.refresh(milestone)
        return milestone

    def delete_milestone(self, milestone_id):
        milestone = self.db.query(Milestone).get(milestone_id)
        if not milestone:
            return False
        self.db.delete(milestone)
        self.db.commit()
        return True
