from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.device import DeviceCreate
from app.crud.device import create_device, get_device, get_devices_by_user
from app.database.db import get_db

router = APIRouter(prefix="/devices", tags=["Devices"])

@router.post("/")
def create(device: DeviceCreate, db: Session = Depends(get_db)):
    return create_device(db, device)

@router.get("/{device_id}")
def read(device_id: int, db: Session = Depends(get_db)):
    return get_device(db, device_id)

@router.get("/user/{user_id}")
def read_by_user(user_id: int, db: Session = Depends(get_db)):
    return get_devices_by_user(db, user_id)