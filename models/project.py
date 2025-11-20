from pydantic import BaseModel
from typing import List, Optional

class ProjectBase(BaseModel):
    title: str
    description: str

class ProjectCreate(ProjectBase):
    pass

class ProjectResponse(ProjectBase):
    id: int

class Project(ProjectBase):
    id: int