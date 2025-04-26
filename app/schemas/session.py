from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class SessionBase(BaseModel):
    user_id: int
    token: str
    ip_address: str
    device_info: str

class SessionCreate(SessionBase):
    expires_at: Optional[datetime] = None

class SessionUpdate(BaseModel):
    user_id: Optional[int] = None
    token: Optional[str] = None
    ip_address: Optional[str] = None
    device_info: Optional[str] = None
    expires_at: Optional[datetime] = None

class Session(SessionBase):
    session_id: int
    expires_at: datetime
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)