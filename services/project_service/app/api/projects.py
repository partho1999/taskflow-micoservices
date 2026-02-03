from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List
from app.api.dependencies import require_org_role, get_current_user
from app.db.session import get_db
from app.db.models.project import Project
from app.schemas.project import ProjectCreate, ProjectOut, ProjectOutSimple

router = APIRouter()

@router.post("/{org_id}/projects", response_model=ProjectOut)
async def create_project(
    org_id: str,
    payload: ProjectCreate,
    user_info: dict = Depends(require_org_role(["owner", "admin"])),
    db: Session = Depends(get_db)
):
    """
    Create a project if the user is owner/admin in the org.
    Auto-generates slug and ensures unique project name per organization.
    """

    # Check if project name exists in the same org
    existing_project = db.query(Project).filter_by(name=payload.name, org_id=org_id).first()
    if existing_project:
        raise HTTPException(
            status_code=400,
            detail=f"Project name '{payload.name}' already exists in this organization"
        )

    # Create project
    project = Project(
        name=payload.name,
        description=payload.description,
        org_id=org_id,
        owner_id=user_info["user_id"],
        extra=payload.extra  # 🔹 Updated to match your model
    )

    db.add(project)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Project slug already exists. Try a different name."
        )

    db.refresh(project)

    return project


# -----------------------------
# Get all projects of logged-in user
# -----------------------------
@router.get("/my-projects", response_model=list[ProjectOutSimple])
def get_my_projects(
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Get all projects owned by logged-in user
    """
    projects = (
        db.query(Project)
        .filter(Project.owner_id == user["user_id"])
        .order_by(Project.created_at.desc())
        .all()
    )

    return projects

# -----------------------------
# Get a single project by ID
# -----------------------------
@router.get("/{project_id}", response_model=ProjectOut)
async def get_project_by_id(
    project_id: str,
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Get a project by project_id.
    Checks if the logged-in user is allowed to view the project
    (owner or member).
    """
    # Fetch project
    project = db.query(Project).filter(Project.id == project_id).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Check permission: owner or member
    is_member = any(m.user_id == user["user_id"] for m in project.members)

    if project.owner_id != user["user_id"] and not is_member:
        raise HTTPException(
            status_code=403,
            detail="You are not allowed to access this project"
        )

    return project