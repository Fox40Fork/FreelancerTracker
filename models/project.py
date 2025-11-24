from pydantic import BaseModel
from typing import Optional

class ProjectBase(BaseModel):
    client_id: int
    user_id: int
    title: str
    description: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectResponse(ProjectBase):
    id: int

class Project(ProjectBase):
    id: int