from sqlalchemy.orm import Session
from app.models.device import Device
from app.schemas.device import DeviceCreate

def create_device(db: Session, device: DeviceCreate):
    db_device = Device(**device.dict())
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device

def get_device(db: Session, device_id: int):
    return db.query(Device).filter(Device.device_id == device_id).first()

def get_devices_by_user(db: Session, user_id: int):
    return db.query(Device).filter(Device.user_id == user_id).all()