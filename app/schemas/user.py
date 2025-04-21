from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime

class UserBase(BaseModel):
    name: str
    email: EmailStr
    phone: str
    address: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    user_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

# UserUpdate schema that allows for optional fields
class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    address: str | None = None

    model_config = ConfigDict(from_attributes=True)
