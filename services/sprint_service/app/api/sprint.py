from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List
from app.db.session import get_db
from app.schemas.sprint import SprintCreate, SprintRead, SprintUpdate
from app.services.sprint_service import SprintService
from app.api.dependencies import get_current_user

router = APIRouter(tags=["Sprints"])


@router.post("/", response_model=SprintRead, status_code=status.HTTP_201_CREATED)
def create_sprint(
    sprint_in: SprintCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    service = SprintService(db)
    sprint = service.create_sprint(sprint_in, user_id=user["id"])
    return sprint


@router.get("/", response_model=List[SprintRead])
def list_sprints(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    service = SprintService(db)
    return service.get_sprints(skip, limit)


@router.get("/{sprint_id}", response_model=SprintRead)
def get_sprint(sprint_id: UUID, db: Session = Depends(get_db)):
    service = SprintService(db)
    sprint = service.get_sprint(sprint_id)
    if not sprint:
        raise HTTPException(status_code=404, detail="Sprint not found")
    return sprint


@router.patch("/{sprint_id}", response_model=SprintRead)
def update_sprint(
    sprint_id: UUID,
    sprint_in: SprintUpdate,
    db: Session = Depends(get_db),
):
    service = SprintService(db)
    sprint = service.update_sprint(sprint_id, sprint_in)
    if not sprint:
        raise HTTPException(status_code=404, detail="Sprint not found")
    return sprint


@router.delete("/{sprint_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sprint(sprint_id: UUID, db: Session = Depends(get_db)):
    service = SprintService(db)
    success = service.delete_sprint(sprint_id)
    if not success:
        raise HTTPException(status_code=404, detail="Sprint not found")
    return
