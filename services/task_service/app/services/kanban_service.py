from sqlalchemy.orm import Session
from typing import Dict, List
from app.models.task import Task, TaskStatus
from app.schemas.task import TaskOut


class KanbanService:
    def __init__(self, db: Session):
        self.db = db

    def get_board(self, project_id: str) -> Dict[str, List[TaskOut]]:
        board = {status.value: [] for status in TaskStatus}

        tasks = (
            self.db.query(Task)
            .filter(
                Task.project_id == project_id,
                Task.is_deleted == False
            )
            .all()
        )

        for task in tasks:
            board[task.status.value].append(
                TaskOut.model_validate(task)  # ✅ KEY FIX
            )

        # Sort by position
        for col in board.values():
            col.sort(key=lambda t: t.position)

        return board

    def move_task(self, task_id: str, new_status: str, new_position: int = 0):
        task = self.db.query(Task).filter(Task.id == task_id).first()
        if not task:
            return None

        task.status = TaskStatus(new_status)
        task.position = new_position

        self.db.commit()
        self.db.refresh(task)

        return TaskOut.model_validate(task)  # ✅ also convert here
