from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.dependencies import get_current_user
from app.services.leaderboard_service import LeaderBoardService

router = APIRouter(tags=["LeaderBoard"])

@router.get("/{project_id}")
def get_leaderboard(
    project_id: str, 
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
    ):
    service = LeaderBoardService(db)
    return service.get_leaderboard(project_id)
