from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.subscription import SubscriptionCreate
from app.crud.subscription import create_subscription, get_subscription
from app.database.db import get_db

router = APIRouter(prefix="/subscriptions", tags=["Subscriptions"])

@router.post("/")
def create(subscription: SubscriptionCreate, db: Session = Depends(get_db)):
    return create_subscription(db, subscription)

@router.get("/{subscription_id}")
def read(subscription_id: int, db: Session = Depends(get_db)):
    return get_subscription(db, subscription_id)
