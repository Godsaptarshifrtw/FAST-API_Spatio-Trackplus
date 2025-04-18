from sqlalchemy.orm import Session
from app.models.session import Session as SessionModel
from app.schemas.session import SessionCreate

def create_session(db: Session, session: SessionCreate):
    db_session = SessionModel(**session.dict())
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

def get_session(db: Session, session_id: int):
    return db.query(SessionModel).filter(SessionModel.session_id == session_id).first()
