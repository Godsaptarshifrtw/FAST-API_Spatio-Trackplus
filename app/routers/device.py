from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.db import get_db
from app.schemas.device import DeviceCreate, Device
from app.models.device import Device as DeviceModel
from app.models.user import User as UserModel
from app.models.subscription import Subscription as SubscriptionModel
from datetime import datetime

router = APIRouter()

@router.post("/", response_model=Device)
def create_device(device: DeviceCreate, db: Session = Depends(get_db)):
    # Check if user exists
    user = db.query(UserModel).filter(UserModel.user_id == device.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # If subscription_id is provided, check if it exists
    if device.subscription_id is not None:
        subscription = db.query(SubscriptionModel).filter(SubscriptionModel.subscription_id == device.subscription_id).first()
        if not subscription:
            raise HTTPException(status_code=404, detail="Subscription not found")
    
    # Create new device
    db_device = DeviceModel(
        user_id=device.user_id,
        subscription_id=device.subscription_id,
        imei_number=device.imei_number,
        device_type=device.device_type,
        model=device.model,
        status=device.status,
        added_on=datetime.utcnow()
    )
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device

@router.get("/{device_id}", response_model=Device)
def get_device(device_id: int, db: Session = Depends(get_db)):
    db_device = db.query(DeviceModel).filter(DeviceModel.device_id == device_id).first()
    if db_device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    return db_device

@router.get("/user/{user_id}", response_model=List[Device])
def get_user_devices(user_id: int, db: Session = Depends(get_db)):
    devices = db.query(DeviceModel).filter(DeviceModel.user_id == user_id).all()
    return devices

@router.get("/", response_model=List[Device])
def get_devices(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    devices = db.query(DeviceModel).offset(skip).limit(limit).all()
    return devices

@router.delete("/{device_id}")
def delete_device(device_id: int, db: Device = Depends(get_db)):
    db_device = db.query(DeviceModel).filter(UserModel.user_id == device_id).first()
    if db_device is None:
        raise HTTPException(status_code=404, detail="device not found")
    db.delete(db_device)
    db.commit()
    return {"message": "device deleted successfully"}
