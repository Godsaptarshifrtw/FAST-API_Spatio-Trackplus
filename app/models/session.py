from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime, timedelta
from app.database.session_db import Base

class Session(Base):
    __tablename__ = "sessions"

    session_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    token = Column(String)
    ip_address = Column(String)
    device_info = Column(String)
    expires_at = Column(DateTime, default=datetime.utcnow() + timedelta(hours=1))
    created_at = Column(DateTime, default=datetime.utcnow)
