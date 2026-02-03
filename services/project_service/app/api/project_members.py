from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.db.session import get_db
from app.db.models.project_member import ProjectMember
from app.db.models.project import Project
from app.schemas.project_member import MemberCreate, MemberResponse
from typing import List
from app.api.dependencies import get_current_user  # your JWT auth

router = APIRouter()


@router.post("/{project_id}/members", response_model=MemberResponse)
async def add_member(
    project_id: str,
    payload: MemberCreate,
    user_info: dict = Depends(get_current_user),  # only authentication
    db: Session = Depends(get_db)
):
    # Check if project exists
    project = db.query(Project).filter_by(id=project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Check if member already exists
    existing_member = db.query(ProjectMember).filter_by(project_id=project_id, user_id=payload.user_id).first()
    if existing_member:
        raise HTTPException(status_code=400, detail=f"User {payload.user_id} is already a member of this project")

    # Add member
    member = ProjectMember(
        project_id=project_id,
        user_id=payload.user_id,
        role=payload.role
    )

    db.add(member)
    try:
        db.commit()
        db.refresh(member)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Failed to add member due to DB conflict")

    return member


@router.get("/{project_id}/members", response_model=List[MemberResponse])
async def list_members(
    project_id: str,
    user_info: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check if project exists
    project = db.query(Project).filter_by(id=project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    members = db.query(ProjectMember).filter_by(project_id=project_id).all()
    return members
