from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.task import Task, TaskPriority
from typing import List, Dict

class LeaderBoardService:
    def __init__(self, db: Session):
        self.db = db

    def get_leaderboard(self, project_id: str) -> List[Dict]:
        tasks = (
            self.db.query(Task.assignee_id, Task.priority)
            .filter(Task.project_id == project_id, Task.status == "done", Task.is_deleted == False)
            .all()
        )
        points_map = {"low": 1, "medium": 2, "high": 3, "urgent": 5}
        leaderboard: Dict[str, Dict] = {}
        for assignee_id, priority in tasks:
            if assignee_id not in leaderboard:
                leaderboard[assignee_id] = {"user_id": assignee_id, "completed_tasks": 0, "points": 0}
            leaderboard[assignee_id]["completed_tasks"] += 1
            leaderboard[assignee_id]["points"] += points_map[priority.value]
        return sorted(leaderboard.values(), key=lambda x: x["points"], reverse=True)
