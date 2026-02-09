# app/api/milestone.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.db.session import get_db
from app.services.milestone_service import MilestoneService
from app.schemas.milestone import (
    MilestoneCreate,
    MilestoneUpdate,
    MilestoneOut
)
from app.api.dependencies import get_current_user

router = APIRouter(tags=["Milestones"])


@router.post("/{sprint_id}", response_model=MilestoneOut)
def create_milestone(
    sprint_id: UUID,
    data: MilestoneCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    service = MilestoneService(db)
    return service.create_milestone(sprint_id, data)


@router.get("/sprint/{sprint_id}", response_model=list[MilestoneOut])
def get_milestones(
    sprint_id: UUID,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    service = MilestoneService(db)
    return service.get_sprint_milestones(sprint_id)


@router.get("/{milestone_id}", response_model=MilestoneOut)
def get_milestone(
    milestone_id: UUID,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    service = MilestoneService(db)
    milestone = service.get_milestone(milestone_id)

    if not milestone:
        raise HTTPException(status_code=404, detail="Milestone not found")

    return milestone

@router.patch("/{milestone_id}", response_model=MilestoneOut)
def update_milestone(
    milestone_id: UUID,
    data: MilestoneUpdate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    service = MilestoneService(db)
    milestone = service.update_milestone(milestone_id, data)

    if not milestone:
        raise HTTPException(status_code=404, detail="Milestone not found")

    return milestone


@router.delete("/{milestone_id}")
def delete_milestone(
    milestone_id: UUID,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    service = MilestoneService(db)
    deleted = service.delete_milestone(milestone_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Milestone not found")

    return {"message": "Milestone deleted successfully"}
