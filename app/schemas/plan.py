from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class PlanBase(BaseModel):
    product_id: int
    name: str
    price: float
    duration_days: int
    features: Optional[dict]
    is_active: bool

class PlanCreate(PlanBase):
    pass

class PlanUpdate(BaseModel):
    product_id: Optional[int] = None
    name: Optional[str] = None
    price: Optional[float] = None
    duration_days: Optional[int] = None
    features: Optional[dict] = None
    is_active: Optional[bool] = None

class Plan(PlanBase):
    plan_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
