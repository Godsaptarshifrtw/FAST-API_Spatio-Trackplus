from pydantic import BaseModel
from datetime import datetime

class DeviceBase(BaseModel):
    user_id: int
    subscription_id: int
    imei_number: str
    device_type: str
    model: str
    status: str

class DeviceCreate(DeviceBase):
    pass

class Device(DeviceBase):
    device_id: int
    added_on: datetime

    class Config:
        orm_mode = True