from sqlalchemy.orm import Session
from app.models.subtask import Subtask
from app.schemas.subtask import SubtaskCreate, SubtaskUpdate

class SubtaskService:
    def __init__(self, db: Session):
        self.db = db

    def create_subtask(self, subtask_in: SubtaskCreate) -> Subtask:
        subtask = Subtask(**subtask_in.dict())
        self.db.add(subtask)
        self.db.commit()
        self.db.refresh(subtask)
        return subtask

    def get_subtask(self, subtask_id: str) -> Subtask:
        return self.db.query(Subtask).filter(Subtask.id == subtask_id, Subtask.is_deleted == False).first()

    def list_subtasks(self, task_id: str):
        return self.db.query(Subtask).filter(Subtask.task_id == task_id, Subtask.is_deleted == False).all()

    def update_subtask(self, subtask_id: str, subtask_in: SubtaskUpdate) -> Subtask:
        subtask = self.get_subtask(subtask_id)
        if not subtask:
            return None
        for field, value in subtask_in.dict(exclude_unset=True).items():
            setattr(subtask, field, value)
        self.db.commit()
        self.db.refresh(subtask)
        return subtask

    def delete_subtask(self, subtask_id: str):
        subtask = self.get_subtask(subtask_id)
        if not subtask:
            return None
        subtask.is_deleted = True
        self.db.commit()
        return subtask
