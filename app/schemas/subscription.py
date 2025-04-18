from pydantic import BaseModel
from datetime import date, datetime

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

class Subscription(SubscriptionBase):
    subscription_id: int
    created_at: datetime

    class Config:
        orm_mode = True