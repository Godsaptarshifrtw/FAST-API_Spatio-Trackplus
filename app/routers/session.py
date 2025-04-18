from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.database.session_db import get_db
from app.auth import session as session_utils
from app.schemas.session import Session as SessionSchema

router = APIRouter(prefix="/sessions", tags=["Sessions"])


@router.post("/login", response_model=SessionSchema)
def login(user_id: int, request: Request, db: Session = Depends(get_db)):
    ip = request.client.host
    device_info = request.headers.get("user-agent", "Unknown Device")
    return session_utils.create_session(db, user_id=user_id, ip_address=ip, device_info=device_info)

@router.get("/me/{token}", response_model=SessionSchema)
def get_session(token: str, db: Session = Depends(get_db)):
    session = session_utils.get_session_by_token(db, token)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session

@router.delete("/logout/{token}")
def logout(token: str, db: Session = Depends(get_db)):
    success = session_utils.delete_session(db, token)
    if not success:
        raise HTTPException(status_code=404, detail="Session not found or already logged out")
    return {"message": "Logged out successfully"}

@router.get("/user/{user_id}", response_model=list[SessionSchema])
def get_user_sessions(user_id: int, db: Session = Depends(get_db)):
    return session_utils.get_active_sessions_for_user(db, user_id)
