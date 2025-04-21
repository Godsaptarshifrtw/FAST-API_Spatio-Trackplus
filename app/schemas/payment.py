from pydantic import BaseModel, ConfigDict
from datetime import datetime

class PaymentBase(BaseModel):
    user_id: int
    plan_id: int
    amount: float
    payment_method: str
    status: str
    transaction_id: str

class PaymentCreate(PaymentBase):
    pass

class Payment(PaymentBase):
    payment_id: int
    payment_date: datetime

    model_config = ConfigDict(from_attributes=True)