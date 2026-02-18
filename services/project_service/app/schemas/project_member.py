from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class MemberBase(BaseModel):
    user_id: str
    role: Optional[str] = "member"

class MemberCreate(MemberBase):
    pass

class MemberResponse(MemberBase):
    id: str
    project_id: str
    created_at: datetime

    model_config = {
        "from_attributes": True  # Pydantic v2
    }
