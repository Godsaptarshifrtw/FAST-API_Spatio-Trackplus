from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate
from app.crud.user import create_user, get_user, get_users
from app.database.db import get_db

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/")
def create(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user)

@router.get("/{user_id}")
def read(user_id: int, db: Session = Depends(get_db)):
    return get_user(db, user_id)

@router.get("/")
def read_all(db: Session = Depends(get_db)):
    return get_users(db)