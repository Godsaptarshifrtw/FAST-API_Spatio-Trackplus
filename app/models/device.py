from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from app.database.db import Base

class Device(Base):
    __tablename__ = "devices"

    device_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    subscription_id = Column(Integer, ForeignKey("subscriptions.subscription_id"))
    imei_number = Column(String, nullable=False)
    device_type = Column(String)
    model = Column(String)
    status = Column(String)
    added_on = Column(DateTime, default=datetime.utcnow)