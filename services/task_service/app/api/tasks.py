# api/tasks.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from fastapi import Query
from app.db.session import get_db
from app.services.task_service import TaskService
from app.schemas.task import TaskCreate, TaskOut, TaskUpdate, AssignSprintToTasks
from app.models.task import TaskStatus, Task

# Dependencies for auth & project
from app.api.dependencies import get_current_user, check_project

router = APIRouter(tags=["Tasks"])


# -----------------------------
# Dependency to get TaskService
# -----------------------------
def get_task_service(db: Session = Depends(get_db)) -> TaskService:
    return TaskService(db)

# -----------------------------
# Bulk assign a sprint_id
# -----------------------------
@router.patch("/assign-sprint")
def assign_sprint_to_tasks(
    payload: AssignSprintToTasks,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    """
    Bulk assign sprint_id to multiple tasks.
    Only updates tasks that exist.
    """

    # Fetch tasks whose IDs are in payload.task_ids
    tasks = db.query(Task).filter(Task.id.in_(payload.task_ids)).all()

    if not tasks:
        raise HTTPException(status_code=404, detail="Tasks not found")

    # Update sprint_id for all tasks
    for task in tasks:
        task.sprint_id = payload.sprint_id

    db.commit()

    return {
        "message": f"Sprint {payload.sprint_id} assigned to {len(tasks)} task(s) successfully."
    }


# -----------------------------
# Create Task
# -----------------------------
@router.post("/{project_id}", response_model=TaskOut)
def create_task(
    project_id: str,
    task_in: TaskCreate,
    user: dict = Depends(get_current_user),
    project_info: dict = Depends(check_project()),
    service: TaskService = Depends(get_task_service),
):
    """
    Create a task under a specific project.
    - project_id comes from the URL
    - reporter_id comes from JWT
    - Validates project existence using check_project()
    """
    task_in.project_id = UUID(project_id)
    task_in.reporter_id = UUID(user["user_id"])
    return service.create_task(task_in)


# -----------------------------
# Get Single Task
# -----------------------------
@router.get("/{task_id}", response_model=TaskOut)
def get_task(
    task_id: UUID,
    service: TaskService = Depends(get_task_service)
):
    """
    Fetch a single task by ID
    """
    return service.get_task(task_id)


# -----------------------------
# Get Multiple Tasks
# -----------------------------
@router.get("/", response_model=List[TaskOut])
def get_tasks(
    project_id: UUID = None,
    assignee_id: UUID = None,
    sprint_id: UUID | str = None,
    sprint_not_assigned: bool = Query(False, description="Set true to get tasks with no sprint assigned"),
    status: TaskStatus = None,
    skip: int = 0,
    limit: int = 20,
    service: TaskService = Depends(get_task_service),
):
    """
    Fetch multiple tasks with optional filters:
    - project_id: filter by project
    - assignee_id: filter by assignee
    - sprint_id: filter by sprint
    - sprint_not_assigned: filter tasks with no sprint
    - status: filter by status enum
    - skip/limit: pagination
    """
    return service.get_tasks(
        project_id=project_id,
        assignee_id=assignee_id,
        sprint_id=sprint_id,
        sprint_not_assigned=sprint_not_assigned,
        status=status,
        skip=skip,
        limit=limit
    )


# -----------------------------
# Update Task
# -----------------------------
@router.put("/{task_id}", response_model=TaskOut)
def update_task(
    task_id: UUID,
    task_in: TaskUpdate,
    user: dict = Depends(get_current_user),
    service: TaskService = Depends(get_task_service),
):
    """
    Update a task partially. Only fields sent in the request will be updated.
    """
    return service.update_task(task_id, task_in)

@router.patch("/{task_id}", response_model=TaskOut)
def update_task(
    task_id: UUID,
    task_in: TaskUpdate,
    user: dict = Depends(get_current_user),
    service: TaskService = Depends(get_task_service),
):
    """
    Partially update a task. Only fields sent in the request will be updated.
    """
    return service.update_task(task_id, task_in)


# -----------------------------
# Delete Task (Soft Delete)
# -----------------------------
@router.delete("/{task_id}")
def delete_task(
    task_id: UUID,
    user: dict = Depends(get_current_user),
    service: TaskService = Depends(get_task_service),
):
    """
    Soft delete a task. Marks is_deleted=True.
    """
    service.delete_task(task_id)
    return {"detail": "Task deleted"}
