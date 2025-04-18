from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.session import Session as SessionModel
from app.schemas.session import SessionCreate
import uuid

SESSION_EXPIRY_HOURS = 12  # you can adjust this

def create_session(db: Session, user_id: int, ip_address: str, device_info: str) -> SessionModel:
    token = str(uuid.uuid4())
    expires_at = datetime.utcnow() + timedelta(hours=SESSION_EXPIRY_HOURS)
    
    session_data = SessionModel(
        user_id=user_id,
        token=token,
        ip_address=ip_address,
        device_info=device_info,
        expires_at=expires_at,
        created_at=datetime.utcnow()
    )
    db.add(session_data)
    db.commit()
    db.refresh(session_data)
    return session_data


def get_session_by_token(db: Session, token: str) -> SessionModel | None:
    return db.query(SessionModel).filter(SessionModel.token == token).first()


def delete_session(db: Session, token: str) -> bool:
    session_obj = get_session_by_token(db, token)
    if session_obj:
        db.delete(session_obj)
        db.commit()
        return True
    return False


def get_active_sessions_for_user(db: Session, user_id: int):
    return db.query(SessionModel).filter(
        SessionModel.user_id == user_id,
        SessionModel.expires_at > datetime.utcnow()
    ).all()
