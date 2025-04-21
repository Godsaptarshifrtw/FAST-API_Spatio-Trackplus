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

class Plan(PlanBase):
    plan_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
