from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List
from app.database.session_db import get_db
from app.auth import session as session_utils
from app.schemas.session import Session as SessionSchema, SessionCreate
from app.models.session import Session as SessionModel
from app.models.user import User as UserModel
from datetime import datetime, timedelta

router = APIRouter()


@router.post("/", response_model=SessionSchema)
def create_session(session: SessionCreate, db: Session = Depends(get_db)):
    # Check if user exists
    user = db.query(UserModel).filter(UserModel.user_id == session.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Create new session
    db_session = SessionModel(
        user_id=session.user_id,
        token=session.token,
        ip_address=session.ip_address,
        device_info=session.device_info,
        expires_at=datetime.utcnow() + timedelta(days=1),  # Default 1 day expiration
        created_at=datetime.utcnow()
    )
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

@router.get("/{session_id}", response_model=SessionSchema)
def get_session(session_id: int, db: Session = Depends(get_db)):
    db_session = db.query(SessionModel).filter(SessionModel.session_id == session_id).first()
    if db_session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    return db_session

@router.get("/user/{user_id}", response_model=List[SessionSchema])
def get_user_sessions(user_id: int, db: Session = Depends(get_db)):
    sessions = db.query(SessionModel).filter(SessionModel.user_id == user_id).all()
    return sessions

@router.get("/active/{user_id}", response_model=List[SessionSchema])
def get_active_sessions(user_id: int, db: Session = Depends(get_db)):
    current_time = datetime.utcnow()
    sessions = db.query(SessionModel).filter(
        SessionModel.user_id == user_id,
        SessionModel.expires_at > current_time
    ).all()
    return sessions

@router.delete("/{session_id}")
def delete_session(session_id: int, db: Session = Depends(get_db)):
    db_session = db.query(SessionModel).filter(SessionModel.session_id == session_id).first()
    if db_session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    db.delete(db_session)
    db.commit()
    return {"message": "Session deleted successfully"}
