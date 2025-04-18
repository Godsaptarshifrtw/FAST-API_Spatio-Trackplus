from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, JSON, ForeignKey
from datetime import datetime
from app.database.db import Base

class Plan(Base):
    __tablename__ = "plans"

    plan_id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer)
    name = Column(String)
    price = Column(Float)
    duration_days = Column(Integer)
    features = Column(JSON)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)