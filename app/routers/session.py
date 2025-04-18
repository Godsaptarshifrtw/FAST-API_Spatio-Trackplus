from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.session import SessionCreate
from app.crud.session import create_session, get_session
from app.database.session_db import get_session_db

router = APIRouter(prefix="/sessions", tags=["Sessions"])

@router.post("/")
def create(session: SessionCreate, db: Session = Depends(get_session_db)):
    return create_session(db, session)

@router.get("/{session_id}")
def read(session_id: int, db: Session = Depends(get_session_db)):
    return get_session(db, session_id)
