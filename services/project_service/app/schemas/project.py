from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None
    extra: Optional[Dict[str, Any]] = None  # matches your model

class ProjectOut(ProjectCreate):
    id: str
    slug: str
    org_id: str
    owner_id: str
    created_at: datetime

    model_config = {
        "from_attributes": True  # for Pydantic v2
    }

class ProjectOutSimple(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    slug: str
    org_id: str
    owner_id: str
    created_at: datetime

    model_config = {
        "from_attributes": True  # Pydantic v2
    }
