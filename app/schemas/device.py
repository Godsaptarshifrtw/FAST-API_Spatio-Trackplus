from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class DeviceBase(BaseModel):
    user_id: int
    subscription_id: Optional[int] = None
    imei_number: str
    device_type: str
    model: str
    status: str

class DeviceCreate(DeviceBase):
    pass

class DeviceUpdate(BaseModel):
    user_id: Optional[int] = None
    subscription_id: Optional[int] = None
    imei_number: Optional[str] = None
    device_type: Optional[str] = None
    model: Optional[str] = None
    status: Optional[str] = None

class Device(DeviceBase):
    device_id: int
    added_on: datetime

    model_config = ConfigDict(from_attributes=True)