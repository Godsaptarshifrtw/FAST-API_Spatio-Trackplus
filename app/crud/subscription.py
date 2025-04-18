from sqlalchemy.orm import Session
from app.models.subscription import Subscription
from app.schemas.subscription import SubscriptionCreate

def create_subscription(db: Session, subscription: SubscriptionCreate):
    db_subscription = Subscription(**subscription.dict())
    db.add(db_subscription)
    db.commit()
    db.refresh(db_subscription)
    return db_subscription

def get_subscription(db: Session, subscription_id: int):
    return db.query(Subscription).filter(Subscription.subscription_id == subscription_id).first()