# app/api/progress.py
from fastapi import APIRouter, Depends
from app.services.progress_service import get_sprint_progress
from app.api.dependencies import get_current_user

router = APIRouter(tags=["Progress"])


@router.get("/{sprint_id}")
def sprint_progress(
    sprint_id: str,
    user: dict = Depends(get_current_user)

):

    return get_sprint_progress(sprint_id, token=user["token"])
