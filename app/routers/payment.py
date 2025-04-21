from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.db import get_db
from app.schemas.payment import PaymentCreate, Payment
from app.models.payment import Payment as PaymentModel
from app.models.user import User as UserModel
from app.models.plan import Plan as PlanModel
from datetime import datetime
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/test")
def test_endpoint():
    logger.info("Test endpoint called")
    return {"message": "Payment router is working"}

@router.post("/", response_model=Payment)
def create_payment(payment: PaymentCreate, db: Session = Depends(get_db)):
    logger.info(f"Creating payment with data: {payment.model_dump()}")
    
    # Check if user exists
    user = db.query(UserModel).filter(UserModel.user_id == payment.user_id).first()
    if not user:
        logger.error(f"User not found: {payment.user_id}")
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if plan exists
    plan = db.query(PlanModel).filter(PlanModel.plan_id == payment.plan_id).first()
    if not plan:
        logger.error(f"Plan not found: {payment.plan_id}")
        raise HTTPException(status_code=404, detail="Plan not found")
    
    # Create new payment
    db_payment = PaymentModel(
        user_id=payment.user_id,
        plan_id=payment.plan_id,
        amount=payment.amount,
        payment_method=payment.payment_method,
        status=payment.status,
        transaction_id=payment.transaction_id,
        payment_date=datetime.utcnow()
    )
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    logger.info(f"Payment created successfully: {db_payment.payment_id}")
    return db_payment

@router.get("/{payment_id}", response_model=Payment)
def get_payment(payment_id: int, db: Session = Depends(get_db)):
    db_payment = db.query(PaymentModel).filter(PaymentModel.payment_id == payment_id).first()
    if db_payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return db_payment

@router.get("/user/{user_id}", response_model=List[Payment])
def get_user_payments(user_id: int, db: Session = Depends(get_db)):
    payments = db.query(PaymentModel).filter(PaymentModel.user_id == user_id).all()
    return payments

@router.get("/subscription/{subscription_id}", response_model=List[Payment])
def get_subscription_payments(subscription_id: int, db: Session = Depends(get_db)):
    payments = db.query(PaymentModel).filter(PaymentModel.subscription_id == subscription_id).all()
    return payments