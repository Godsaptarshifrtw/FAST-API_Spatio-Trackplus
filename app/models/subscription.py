from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Date
from datetime import datetime
from app.database.db import Base

class Subscription(Base):
    __tablename__ = "subscriptions"

    subscription_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    plan_id = Column(Integer, ForeignKey("plans.plan_id"), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    status = Column(String(50), nullable=False)
    renewal_type = Column(String(50), nullable=False)
    payment_id = Column(Integer, ForeignKey("payments.payment_id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<Subscription {self.subscription_id}>"