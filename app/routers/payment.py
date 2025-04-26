from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database.db import get_db
from app.schemas.payment import PaymentCreate, Payment, PaymentUpdate
from app.models.payment import Payment as PaymentModel
from app.models.user import User as UserModel
from app.models.plan import Plan as PlanModel
from app.auth.auth import get_current_user
from datetime import datetime
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/test")
def test_endpoint():
    logger.info("Test endpoint called")
    return {"message": "Payment router is working"}

@router.post("/", response_model=Payment)
def create_payment(payment: PaymentCreate, 
                  db: Session = Depends(get_db),
                  current_user: UserModel = Depends(get_current_user)):
    # Create new payment
    db_payment = PaymentModel(
        user_id=payment.user_id,
        amount=payment.amount,
        payment_method=payment.payment_method,
        status=payment.status,
        transaction_id=payment.transaction_id,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment

@router.get("/{payment_id}", response_model=Payment)
def get_payment(payment_id: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching payment with ID: {payment_id}")
    db_payment = db.query(PaymentModel).filter(PaymentModel.payment_id == payment_id).first()
    if db_payment is None:
        logger.warning(f"Payment not found with ID: {payment_id}")
        raise HTTPException(status_code=404, detail="Payment not found")
    return db_payment

@router.get("/user/{user_id}", response_model=List[Payment])
def get_user_payments(user_id: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching payments for user ID: {user_id}")
    payments = db.query(PaymentModel).filter(PaymentModel.user_id == user_id).all()
    logger.info(f"Found {len(payments)} payments for user {user_id}")
    return payments

@router.get("/subscription/{subscription_id}", response_model=List[Payment])
def get_subscription_payments(subscription_id: int, db: Session = Depends(get_db)):
    payments = db.query(PaymentModel).filter(PaymentModel.subscription_id == subscription_id).all()
    return payments

@router.put("/{payment_id}", response_model=Payment)
def update_payment(payment_id: int, 
                  payment: PaymentUpdate, 
                  db: Session = Depends(get_db),
                  current_user: UserModel = Depends(get_current_user)):
    db_payment = db.query(PaymentModel).filter(PaymentModel.payment_id == payment_id).first()
    if db_payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    
    # Verify user has permission to update this payment
    if db_payment.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this payment")
    
    update_data = payment.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_payment, key, value)
    
    db_payment.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_payment)
    return db_payment

@router.delete("/{payment_id}")
def delete_payment(payment_id: int, 
                  db: Session = Depends(get_db),
                  current_user: UserModel = Depends(get_current_user)):
    db_payment = db.query(PaymentModel).filter(PaymentModel.payment_id == payment_id).first()
    if db_payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    
    # Verify user has permission to delete this payment
    if db_payment.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this payment")
    
    db.delete(db_payment)
    db.commit()
    return {"message": "Payment deleted successfully"}