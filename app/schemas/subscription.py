from pydantic import BaseModel, ConfigDict
from datetime import date, datetime
from typing import Optional

class SubscriptionBase(BaseModel):
    user_id: int
    plan_id: int
    start_date: date
    end_date: date
    status: str
    renewal_type: str
    payment_id: int

class SubscriptionCreate(SubscriptionBase):
    pass

class SubscriptionUpdate(BaseModel):
    user_id: Optional[int] = None
    plan_id: Optional[int] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[str] = None
    renewal_type: Optional[str] = None
    payment_id: Optional[int] = None

class Subscription(SubscriptionBase):
    subscription_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)