from pydantic import BaseModel
from datetime import datetime

class PaymentBase(BaseModel):
    user_id: int
    subscription_id: int
    amount: float
    payment_method: str
    status: str
    transaction_id: str

class PaymentCreate(PaymentBase):
    pass

class Payment(PaymentBase):
    payment_id: int
    payment_date: datetime

    class Config:
        orm_mode = True