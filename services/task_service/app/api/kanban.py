from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.kanban_service import KanbanService
from app.schemas.task import TaskOut
from app.schemas.kanban import KanbanResponse
from app.models.task import TaskStatus
from app.api.dependencies import get_current_user

router = APIRouter(tags=["Kanban"])


@router.get("/{project_id}", response_model=KanbanResponse)
def get_kanban_board(
    project_id: str,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    service = KanbanService(db)
    return service.get_board(project_id)


@router.put("/move/{task_id}", response_model=TaskOut)
def move_task(
    task_id: str,
    new_status: TaskStatus = Query(..., description="New task status"),
    new_position: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    service = KanbanService(db)
    task = service.move_task(task_id, new_status.value, new_position)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task
