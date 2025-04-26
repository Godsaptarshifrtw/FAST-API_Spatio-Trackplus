from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database.db import get_db
from app.schemas.user import UserCreate, User, UserUpdate, UserLogin, Token
from app.models.user import User as UserModel
from app.auth.auth import (
    verify_password, get_password_hash, create_access_token,
    get_current_user
)
from datetime import datetime, timedelta
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/login", response_model=Token)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.email == user_data.email).first()
    if not user or not verify_password(user_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/", response_model=User)
def create_user(user: UserCreate, 
                db: Session = Depends(get_db),
                current_user: UserModel = Depends(get_current_user)):
    # Check if user already exists
    db_user = db.query(UserModel).filter(UserModel.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new user
    hashed_password = get_password_hash(user.password)
    db_user = UserModel(
        email=user.email,
        password_hash=hashed_password,
        full_name=user.full_name,
        is_active=user.is_active,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/me", response_model=User)
def read_users_me(current_user: UserModel = Depends(get_current_user)):
    return current_user

@router.get("/", response_model=List[User])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(UserModel).offset(skip).limit(limit).all()
    return users

@router.get("/{user_id}", response_model=User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.user_id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/{user_id}", response_model=User)
def update_user(user_id: int, 
                user: UserUpdate, 
                db: Session = Depends(get_db),
                current_user: UserModel = Depends(get_current_user)):
    db_user = db.query(UserModel).filter(UserModel.user_id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Verify user has permission to update this user
    if db_user.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this user")
    
    update_data = user.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if key == "password":
            setattr(db_user, "password_hash", get_password_hash(value))
        else:
            setattr(db_user, key, value)
    
    db_user.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/{user_id}")
def delete_user(user_id: int, 
                db: Session = Depends(get_db),
                current_user: UserModel = Depends(get_current_user)):
    db_user = db.query(UserModel).filter(UserModel.user_id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Verify user has permission to delete this user
    if db_user.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this user")
    
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted successfully"}
