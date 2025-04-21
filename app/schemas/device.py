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

class Device(DeviceBase):
    device_id: int
    added_on: datetime

    model_config = ConfigDict(from_attributes=True)