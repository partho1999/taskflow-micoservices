from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.subtask import SubtaskCreate, SubtaskUpdate, SubtaskRead
from app.services.subtask_service import SubtaskService
from app.db.session import get_db
from app.api.dependencies import get_current_user  

router = APIRouter(tags=["Subtasks"])

@router.post("/", response_model=SubtaskRead)
def create_subtask(
    subtask_in: SubtaskCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)  # authentication
):
    service = SubtaskService(db)
    return service.create_subtask(subtask_in)

@router.get("/task/{task_id}", response_model=List[SubtaskRead])
def list_subtasks(
    task_id: str,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    service = SubtaskService(db)
    return service.list_subtasks(task_id)

@router.get("/{subtask_id}", response_model=SubtaskRead)
def get_subtask(
    subtask_id: str,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    service = SubtaskService(db)
    subtask = service.get_subtask(subtask_id)
    if not subtask:
        raise HTTPException(status_code=404, detail="Subtask not found")
    return subtask

@router.put("/{subtask_id}", response_model=SubtaskRead)
def update_subtask(
    subtask_id: str,
    subtask_in: SubtaskUpdate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    service = SubtaskService(db)
    subtask = service.update_subtask(subtask_id, subtask_in)
    if not subtask:
        raise HTTPException(status_code=404, detail="Subtask not found")
    return subtask

@router.patch("/{subtask_id}", response_model=SubtaskRead)
def update_subtask(
    subtask_id: str,
    subtask_in: SubtaskUpdate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    """
    Partially update a subtask. Only fields sent in the request will be updated.
    """
    service = SubtaskService(db)
    subtask = service.update_subtask(subtask_id, subtask_in)
    if not subtask:
        raise HTTPException(status_code=404, detail="Subtask not found")
    return subtask

@router.delete("/{subtask_id}", response_model=SubtaskRead)
def delete_subtask(
    subtask_id: str,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    service = SubtaskService(db)
    subtask = service.delete_subtask(subtask_id)
    if not subtask:
        raise HTTPException(status_code=404, detail="Subtask not found")
    return subtask
