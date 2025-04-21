from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from datetime import datetime
from app.database.db import Base

class Payment(Base):
    __tablename__ = "payments"

    payment_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    plan_id = Column(Integer, ForeignKey("plans.plan_id"), nullable=False)
    amount = Column(Float, nullable=False)
    payment_method = Column(String(50), nullable=False)
    status = Column(String(50), nullable=False)
    transaction_id = Column(String(100), nullable=False)
    payment_date = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<Payment {self.payment_id}>"