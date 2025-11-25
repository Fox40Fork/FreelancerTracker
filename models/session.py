from pydantic import BaseModel

class SessionBase(BaseModel):
    username: str
class SessionCreate(SessionBase):
    pass
class SessionResponse(SessionBase):
    id: int
class Session(SessionBase):
    id:int