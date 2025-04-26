from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database.db import get_db
from app.schemas.subscription import SubscriptionCreate, Subscription, SubscriptionUpdate
from app.models.subscription import Subscription as SubscriptionModel
from app.models.user import User as UserModel
from app.models.plan import Plan as PlanModel
from app.models.payment import Payment as PaymentModel
from app.auth.auth import get_current_user
from datetime import datetime, timedelta, date
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/test")
def test_endpoint():
    logger.info("Test endpoint called")
    return {"message": "Subscription router is working"}

@router.post("/", response_model=Subscription)
def create_subscription(subscription: SubscriptionCreate, 
                       db: Session = Depends(get_db),
                       current_user: UserModel = Depends(get_current_user)):
    # Verify user exists
    user = db.query(UserModel).filter(UserModel.user_id == subscription.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Verify plan exists
    plan = db.query(PlanModel).filter(PlanModel.plan_id == subscription.plan_id).first()
    if not plan:
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
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(db_subscription)
    db.commit()
    db.refresh(db_subscription)
    logger.info(f"Subscription created successfully: {db_subscription.subscription_id}")
    return db_subscription

@router.get("/{subscription_id}", response_model=Subscription)
def get_subscription(subscription_id: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching subscription with ID: {subscription_id}")
    db_subscription = db.query(SubscriptionModel).filter(SubscriptionModel.subscription_id == subscription_id).first()
    if db_subscription is None:
        logger.warning(f"Subscription not found with ID: {subscription_id}")
        raise HTTPException(status_code=404, detail="Subscription not found")
    return db_subscription

@router.get("/user/{user_id}", response_model=List[Subscription])
def get_user_subscriptions(user_id: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching subscriptions for user ID: {user_id}")
    subscriptions = db.query(SubscriptionModel).filter(SubscriptionModel.user_id == user_id).all()
    logger.info(f"Found {len(subscriptions)} subscriptions for user {user_id}")
    return subscriptions

@router.get("/", response_model=List[Subscription])
def get_subscriptions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    logger.info(f"Fetching subscriptions with skip={skip}, limit={limit}")
    try:
        subscriptions = db.query(SubscriptionModel).offset(skip).limit(limit).all()
        logger.info(f"Found {len(subscriptions)} subscriptions")
        return subscriptions
    except Exception as e:
        logger.error(f"Error in get_subscriptions: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{subscription_id}", response_model=Subscription)
def update_subscription(subscription_id: int, 
                       subscription: SubscriptionUpdate, 
                       db: Session = Depends(get_db),
                       current_user: UserModel = Depends(get_current_user)):
    db_subscription = db.query(SubscriptionModel).filter(SubscriptionModel.subscription_id == subscription_id).first()
    if db_subscription is None:
        raise HTTPException(status_code=404, detail="Subscription not found")
    
    # Verify user has permission to update this subscription
    if db_subscription.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this subscription")
    
    # Check if user exists if user_id is being updated
    if subscription.user_id is not None:
        user = db.query(UserModel).filter(UserModel.user_id == subscription.user_id).first()
        if not user:
            logger.error(f"User not found: {subscription.user_id}")
            raise HTTPException(status_code=404, detail="User not found")
    
    # Check if plan exists if plan_id is being updated
    if subscription.plan_id is not None:
        plan = db.query(PlanModel).filter(PlanModel.plan_id == subscription.plan_id).first()
        if not plan:
            logger.error(f"Plan not found: {subscription.plan_id}")
            raise HTTPException(status_code=404, detail="Plan not found")
    
    # Check if payment exists if payment_id is being updated
    if subscription.payment_id is not None:
        payment = db.query(PaymentModel).filter(PaymentModel.payment_id == subscription.payment_id).first()
        if not payment:
            logger.error(f"Payment not found: {subscription.payment_id}")
            raise HTTPException(status_code=404, detail="Payment not found")
    
    update_data = subscription.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_subscription, key, value)
    
    db_subscription.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_subscription)
    logger.info(f"Subscription {subscription_id} updated successfully")
    return db_subscription

@router.delete("/{subscription_id}")
def delete_subscription(subscription_id: int, 
                       db: Session = Depends(get_db),
                       current_user: UserModel = Depends(get_current_user)):
    db_subscription = db.query(SubscriptionModel).filter(SubscriptionModel.subscription_id == subscription_id).first()
    if db_subscription is None:
        raise HTTPException(status_code=404, detail="Subscription not found")
    
    # Verify user has permission to delete this subscription
    if db_subscription.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this subscription")
    
    db.delete(db_subscription)
    db.commit()
    logger.info(f"Subscription {subscription_id} deleted successfully")
    return {"message": "Subscription deleted successfully"}