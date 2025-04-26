from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List
from app.database.session_db import get_db as get_session_db
from app.database.db import get_db as get_main_db
from app.auth import session as session_utils
from app.schemas.session import Session as SessionSchema, SessionCreate, SessionUpdate
from app.models.session import Session as SessionModel
from app.models.user import User as UserModel
from datetime import datetime, timedelta
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/", response_model=SessionSchema)
def create_session(session: SessionCreate, 
                  session_db: Session = Depends(get_session_db),
                  main_db: Session = Depends(get_main_db)):
    logger.info(f"Creating session with data: {session.model_dump()}")
    # Check if user exists using main database
    user = main_db.query(UserModel).filter(UserModel.user_id == session.user_id).first()
    if not user:
        logger.error(f"User not found: {session.user_id}")
        raise HTTPException(status_code=404, detail="User not found")
    
    # Create new session using session database
    db_session = SessionModel(
        user_id=session.user_id,
        token=session.token,
        ip_address=session.ip_address,
        device_info=session.device_info,
        expires_at=datetime.utcnow() + timedelta(days=1),  # Default 1 day expiration
        created_at=datetime.utcnow()
    )
    session_db.add(db_session)
    session_db.commit()
    session_db.refresh(db_session)
    logger.info(f"Session created successfully: {db_session.session_id}")
    return db_session

@router.get("/{session_id}", response_model=SessionSchema)
def get_session(session_id: int, db: Session = Depends(get_session_db)):
    logger.info(f"Fetching session with ID: {session_id}")
    db_session = db.query(SessionModel).filter(SessionModel.session_id == session_id).first()
    if db_session is None:
        logger.warning(f"Session not found with ID: {session_id}")
        raise HTTPException(status_code=404, detail="Session not found")
    return db_session

@router.get("/user/{user_id}", response_model=List[SessionSchema])
def get_user_sessions(user_id: int, 
                     session_db: Session = Depends(get_session_db),
                     main_db: Session = Depends(get_main_db)):
    logger.info(f"Fetching sessions for user ID: {user_id}")
    # Check if user exists using main database
    user = main_db.query(UserModel).filter(UserModel.user_id == user_id).first()
    if not user:
        logger.error(f"User not found: {user_id}")
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get sessions using session database
    sessions = session_db.query(SessionModel).filter(SessionModel.user_id == user_id).all()
    logger.info(f"Found {len(sessions)} sessions for user {user_id}")
    return sessions

@router.get("/active/{user_id}", response_model=List[SessionSchema])
def get_active_sessions(user_id: int,
                       session_db: Session = Depends(get_session_db),
                       main_db: Session = Depends(get_main_db)):
    logger.info(f"Fetching active sessions for user ID: {user_id}")
    # Check if user exists using main database
    user = main_db.query(UserModel).filter(UserModel.user_id == user_id).first()
    if not user:
        logger.error(f"User not found: {user_id}")
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get active sessions using session database
    current_time = datetime.utcnow()
    sessions = session_db.query(SessionModel).filter(
        SessionModel.user_id == user_id,
        SessionModel.expires_at > current_time
    ).all()
    logger.info(f"Found {len(sessions)} active sessions for user {user_id}")
    return sessions

@router.put("/{session_id}", response_model=SessionSchema)
def update_session(session_id: int, 
                  session: SessionUpdate,
                  session_db: Session = Depends(get_session_db),
                  main_db: Session = Depends(get_main_db)):
    logger.info(f"Updating session with ID: {session_id}")
    db_session = session_db.query(SessionModel).filter(SessionModel.session_id == session_id).first()
    if db_session is None:
        logger.warning(f"Session not found with ID: {session_id}")
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Check if user exists if user_id is being updated
    if session.user_id is not None:
        user = main_db.query(UserModel).filter(UserModel.user_id == session.user_id).first()
        if not user:
            logger.error(f"User not found: {session.user_id}")
            raise HTTPException(status_code=404, detail="User not found")
    
    update_data = session.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_session, key, value)
    
    session_db.commit()
    session_db.refresh(db_session)
    logger.info(f"Session {session_id} updated successfully")
    return db_session

@router.delete("/{session_id}")
def delete_session(session_id: int, db: Session = Depends(get_session_db)):
    logger.info(f"Deleting session with ID: {session_id}")
    db_session = db.query(SessionModel).filter(SessionModel.session_id == session_id).first()
    if db_session is None:
        logger.warning(f"Session not found with ID: {session_id}")
        raise HTTPException(status_code=404, detail="Session not found")
    
    db.delete(db_session)
    db.commit()
    logger.info(f"Session {session_id} deleted successfully")
    return {"message": "Session deleted successfully"}
