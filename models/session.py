from pydantic import BaseModel

class Session(BaseModel):
    session_id: str #this is used for the auth router to create a session that will be deleted on logout/page closing
    username: str