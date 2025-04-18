from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from datetime import datetime
from app.database.db import Base

class Payment(Base):
    __tablename__ = "payments"

    payment_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    subscription_id = Column(Integer, ForeignKey("subscriptions.subscription_id"))
    amount = Column(Float)
    payment_method = Column(String)
    status = Column(String)
    transaction_id = Column(String)
    payment_date = Column(DateTime, default=datetime.utcnow)