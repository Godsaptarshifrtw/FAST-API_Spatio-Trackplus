from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from app.database.db import Base

class Subscription(Base):
    __tablename__ = "subscriptions"

    subscription_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    plan_id = Column(Integer, ForeignKey("plans.plan_id"))
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    status = Column(String)
    renewal_type = Column(String)
    payment_id = Column(Integer, ForeignKey("payments.payment_id"))
    created_at = Column(DateTime, default=datetime.utcnow)