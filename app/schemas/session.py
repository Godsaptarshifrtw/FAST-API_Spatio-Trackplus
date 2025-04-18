from pydantic import BaseModel
from datetime import datetime

class SessionBase(BaseModel):
    user_id: int
    token: str
    ip_address: str
    device_info: str
    expires_at: datetime

class SessionCreate(SessionBase):
    pass

class Session(SessionBase):
    session_id: int
    created_at: datetime

    class Config:
        orm_mode = True