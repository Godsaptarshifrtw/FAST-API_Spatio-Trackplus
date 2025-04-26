from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class PaymentBase(BaseModel):
    user_id: int
    plan_id: int
    amount: float
    payment_method: str
    status: str
    transaction_id: str

class PaymentCreate(PaymentBase):
    pass

class PaymentUpdate(BaseModel):
    user_id: Optional[int] = None
    plan_id: Optional[int] = None
    amount: Optional[float] = None
    payment_method: Optional[str] = None
    status: Optional[str] = None
    transaction_id: Optional[str] = None

class Payment(PaymentBase):
    payment_id: int
    payment_date: datetime

    model_config = ConfigDict(from_attributes=True)