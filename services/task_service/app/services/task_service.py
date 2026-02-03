from sqlalchemy.orm import Session
from app.models.task import Task, TaskStatus
from app.schemas.task import TaskCreate, TaskUpdate
from fastapi import HTTPException
from typing import List
from uuid import UUID

class TaskService:
    def __init__(self, db: Session):
        self.db = db

    # Create task
    def create_task(self, task_in: TaskCreate) -> Task:
        task = Task(**task_in.dict())
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    # Get single task
    def get_task(self, task_id: UUID) -> Task:
        task = self.db.query(Task).filter(Task.id == task_id, Task.is_deleted == False).first()
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return task

    # Get multiple tasks with optional filters
    def get_tasks(
        self,
        project_id: UUID = None,
        assignee_id: UUID = None,
        status: TaskStatus = None,
        skip: int = 0,
        limit: int = 20
    ) -> List[Task]:
        query = self.db.query(Task).filter(
            Task.is_deleted == False,
            Task.sprint_id == None
        )
        if project_id:
            query = query.filter(Task.project_id == project_id)
        if assignee_id:
            query = query.filter(Task.assignee_id == assignee_id)
        if status:
            query = query.filter(Task.status == status)
        return query.offset(skip).limit(limit).all()

    # Update task
    def update_task(self, task_id: UUID, task_in: TaskUpdate) -> Task:
        task = self.get_task(task_id)
        for field, value in task_in.dict(exclude_unset=True).items():
            setattr(task, field, value)
        self.db.commit()
        self.db.refresh(task)
        return task

    # Soft delete task
    def delete_task(self, task_id: UUID) -> None:
        task = self.get_task(task_id)
        task.is_deleted = True
        self.db.commit()
