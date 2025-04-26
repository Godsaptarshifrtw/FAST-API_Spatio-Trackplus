from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.db import get_db
from app.schemas.session import SessionCreate, Session, SessionUpdate
from app.models.session import Session as SessionModel
from app.models.user import User as UserModel
from app.models.device import Device as DeviceModel
from app.auth.auth import get_current_user
from datetime import datetime
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/", response_model=Session)
def create_session(session: SessionCreate, 
                  db: Session = Depends(get_db),
                  current_user: UserModel = Depends(get_current_user)):
    # Verify user exists
    user = db.query(UserModel).filter(UserModel.user_id == session.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Verify device exists
    device = db.query(DeviceModel).filter(DeviceModel.device_id == session.device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    # Create new session
    db_session = SessionModel(
        user_id=session.user_id,
        device_id=session.device_id,
        start_time=session.start_time,
        end_time=session.end_time,
        status=session.status,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

@router.put("/{session_id}", response_model=Session)
def update_session(session_id: int, 
                  session: SessionUpdate, 
                  db: Session = Depends(get_db),
                  current_user: UserModel = Depends(get_current_user)):
    db_session = db.query(SessionModel).filter(SessionModel.session_id == session_id).first()
    if db_session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Verify user has permission to update this session
    if db_session.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this session")
    
    update_data = session.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_session, key, value)
    
    db_session.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_session)
    return db_session

@router.delete("/{session_id}")
def delete_session(session_id: int, 
                  db: Session = Depends(get_db),
                  current_user: UserModel = Depends(get_current_user)):
    db_session = db.query(SessionModel).filter(SessionModel.session_id == session_id).first()
    if db_session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Verify user has permission to delete this session
    if db_session.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this session")
    
    db.delete(db_session)
    db.commit()
    return {"message": "Session deleted successfully"}
