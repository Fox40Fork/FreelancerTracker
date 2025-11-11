from pydantic import BaseModel
from typing import List, Optional

class ClientBase(BaseModel):
    user_id: int
    name: str
    email: Optional[str] = None
    phone: Optional[int] = None
    address: Optional[str] = None

class ClientCreate(ClientBase):
    pass

class ClientResponse(ClientBase):
    id: int

class Client(ClientBase):
    id: int