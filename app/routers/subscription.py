from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.db import get_db
from app.schemas.subscription import SubscriptionCreate, Subscription
from app.models.subscription import Subscription as SubscriptionModel
from app.models.user import User as UserModel
from app.models.plan import Plan as PlanModel
from app.models.payment import Payment as PaymentModel
from datetime import datetime, timedelta, date
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/test")
def test_endpoint():
    logger.info("Test endpoint called")
    return {"message": "Subscription router is working"}

@router.post("/", response_model=Subscription)
def create_subscription(subscription: SubscriptionCreate, db: Session = Depends(get_db)):
    logger.info(f"Creating subscription with data: {subscription.model_dump()}")
    
    # Check if user exists
    user = db.query(UserModel).filter(UserModel.user_id == subscription.user_id).first()
    if not user:
        logger.error(f"User not found: {subscription.user_id}")
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if plan exists
    plan = db.query(PlanModel).filter(PlanModel.plan_id == subscription.plan_id).first()
    if not plan:
        logger.error(f"Plan not found: {subscription.plan_id}")
        raise HTTPException(status_code=404, detail="Plan not found")
    
    # If payment_id is provided, check if it exists
    if subscription.payment_id is not None:
        payment = db.query(PaymentModel).filter(PaymentModel.payment_id == subscription.payment_id).first()
        if not payment:
            logger.error(f"Payment not found: {subscription.payment_id}")
            raise HTTPException(status_code=404, detail="Payment not found")
    
    # Calculate end date based on plan duration if not provided
    if subscription.end_date is None:
        end_date = subscription.start_date + timedelta(days=plan.duration_days)
    else:
        end_date = subscription.end_date
    
    # Create new subscription
    db_subscription = SubscriptionModel(
        user_id=subscription.user_id,
        plan_id=subscription.plan_id,
        start_date=subscription.start_date,
        end_date=end_date,
        status=subscription.status,
        renewal_type=subscription.renewal_type,
        payment_id=subscription.payment_id,
        created_at=datetime.utcnow()
    )
    db.add(db_subscription)
    db.commit()
    db.refresh(db_subscription)
    logger.info(f"Subscription created successfully: {db_subscription.subscription_id}")
    return db_subscription

@router.get("/{subscription_id}", response_model=Subscription)
def get_subscription(subscription_id: int, db: Session = Depends(get_db)):
    db_subscription = db.query(SubscriptionModel).filter(SubscriptionModel.subscription_id == subscription_id).first()
    if db_subscription is None:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return db_subscription

@router.get("/user/{user_id}", response_model=List[Subscription])
def get_user_subscriptions(user_id: int, db: Session = Depends(get_db)):
    subscriptions = db.query(SubscriptionModel).filter(SubscriptionModel.user_id == user_id).all()
    return subscriptions

@router.get("/", response_model=List[Subscription])
def get_subscriptions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    logger.info(f"GET /subscriptions/ endpoint called with skip={skip}, limit={limit}")
    try:
        subscriptions = db.query(SubscriptionModel).offset(skip).limit(limit).all()
        logger.info(f"Found {len(subscriptions)} subscriptions")
        return subscriptions
    except Exception as e:
        logger.error(f"Error in get_subscriptions: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
