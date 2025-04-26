from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.db import get_db
from app.schemas.device import DeviceCreate, Device, DeviceUpdate
from app.models.device import Device as DeviceModel
from app.models.user import User as UserModel
from app.models.subscription import Subscription as SubscriptionModel
from datetime import datetime
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/", response_model=Device)
def create_device(device: DeviceCreate, db: Session = Depends(get_db)):
    logger.info(f"Creating device with data: {device.model_dump()}")
    # Check if user exists
    user = db.query(UserModel).filter(UserModel.user_id == device.user_id).first()
    if not user:
        logger.error(f"User not found: {device.user_id}")
        raise HTTPException(status_code=404, detail="User not found")
    
    # If subscription_id is provided, check if it exists
    if device.subscription_id is not None:
        subscription = db.query(SubscriptionModel).filter(SubscriptionModel.subscription_id == device.subscription_id).first()
        if not subscription:
            logger.error(f"Subscription not found: {device.subscription_id}")
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
    logger.info(f"Device created successfully: {db_device.device_id}")
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
def update_device(device_id: int, device: DeviceUpdate, db: Session = Depends(get_db)):
    logger.info(f"Updating device with ID: {device_id}")
    db_device = db.query(DeviceModel).filter(DeviceModel.device_id == device_id).first()
    if db_device is None:
        logger.warning(f"Device not found with ID: {device_id}")
        raise HTTPException(status_code=404, detail="Device not found")
    
    # Check if user exists if user_id is being updated
    if device.user_id is not None:
        user = db.query(UserModel).filter(UserModel.user_id == device.user_id).first()
        if not user:
            logger.error(f"User not found: {device.user_id}")
            raise HTTPException(status_code=404, detail="User not found")
    
    # Check if subscription exists if subscription_id is being updated
    if device.subscription_id is not None:
        subscription = db.query(SubscriptionModel).filter(SubscriptionModel.subscription_id == device.subscription_id).first()
        if not subscription:
            logger.error(f"Subscription not found: {device.subscription_id}")
            raise HTTPException(status_code=404, detail="Subscription not found")
    
    update_data = device.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_device, key, value)
    
    db.commit()
    db.refresh(db_device)
    logger.info(f"Device {device_id} updated successfully")
    return db_device

@router.delete("/{device_id}")
def delete_device(device_id: int, db: Session = Depends(get_db)):
    logger.info(f"Deleting device with ID: {device_id}")
    db_device = db.query(DeviceModel).filter(DeviceModel.device_id == device_id).first()
    if db_device is None:
        logger.warning(f"Device not found with ID: {device_id}")
        raise HTTPException(status_code=404, detail="Device not found")
    
    db.delete(db_device)
    db.commit()
    logger.info(f"Device {device_id} deleted successfully")
    return {"message": "Device deleted successfully"}
