from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database.db import get_db
from app.schemas.device import DeviceCreate, Device, DeviceUpdate
from app.models.device import Device as DeviceModel
from app.models.user import User as UserModel
from app.models.subscription import Subscription as SubscriptionModel
from app.auth.auth import get_current_user
from datetime import datetime
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/", response_model=Device)
def create_device(device: DeviceCreate, 
                 db: Session = Depends(get_db),
                 current_user: UserModel = Depends(get_current_user)):
    # Verify user exists and has valid subscription
    user = db.query(UserModel).filter(UserModel.user_id == device.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    subscription = db.query(SubscriptionModel).filter(
        SubscriptionModel.user_id == device.user_id,
        SubscriptionModel.status == "active"
    ).first()
    
    if not subscription:
        raise HTTPException(status_code=400, detail="User does not have an active subscription")
    
    # Create new device
    db_device = DeviceModel(
        user_id=device.user_id,
        device_name=device.device_name,
        device_type=device.device_type,
        mac_address=device.mac_address,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device

@router.get("/{device_id}", response_model=Device)
def get_device(device_id: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching device with ID: {device_id}")
    db_device = db.query(DeviceModel).filter(DeviceModel.device_id == device_id).first()
    if db_device is None:
        logger.warning(f"Device not found with ID: {device_id}")
        raise HTTPException(status_code=404, detail="Device not found")
    return db_device

@router.get("/user/{user_id}", response_model=List[Device])
def get_user_devices(user_id: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching devices for user ID: {user_id}")
    devices = db.query(DeviceModel).filter(DeviceModel.user_id == user_id).all()
    logger.info(f"Found {len(devices)} devices for user {user_id}")
    return devices

@router.get("/", response_model=List[Device])
def get_devices(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    logger.info(f"Fetching devices with skip={skip}, limit={limit}")
    devices = db.query(DeviceModel).offset(skip).limit(limit).all()
    logger.info(f"Found {len(devices)} devices")
    return devices

@router.put("/{device_id}", response_model=Device)
def update_device(device_id: int, 
                 device: DeviceUpdate, 
                 db: Session = Depends(get_db),
                 current_user: UserModel = Depends(get_current_user)):
    db_device = db.query(DeviceModel).filter(DeviceModel.device_id == device_id).first()
    if db_device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    
    # Verify user has permission to update this device
    if db_device.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this device")
    
    update_data = device.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_device, key, value)
    
    db_device.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_device)
    return db_device

@router.delete("/{device_id}")
def delete_device(device_id: int, 
                 db: Session = Depends(get_db),
                 current_user: UserModel = Depends(get_current_user)):
    db_device = db.query(DeviceModel).filter(DeviceModel.device_id == device_id).first()
    if db_device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    
    # Verify user has permission to delete this device
    if db_device.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this device")
    
    db.delete(db_device)
    db.commit()
    return {"message": "Device deleted successfully"}
