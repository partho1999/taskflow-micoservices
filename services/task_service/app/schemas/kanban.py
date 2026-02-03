from pydantic import BaseModel
from typing import List, Dict
from app.schemas.task import TaskOut

class KanbanResponse(BaseModel):
    todo: List[TaskOut]
    in_progress: List[TaskOut]
    review: List[TaskOut]
    done: List[TaskOut]
