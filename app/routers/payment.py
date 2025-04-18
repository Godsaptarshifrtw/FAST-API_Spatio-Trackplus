from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.payment import PaymentCreate
from app.crud.payment import create_payment, get_payment
from app.database.db import get_db

router = APIRouter(prefix="/payments", tags=["Payments"])

@router.post("/")
def create(payment: PaymentCreate, db: Session = Depends(get_db)):
    return create_payment(db, payment)

@router.get("/{payment_id}")
def read(payment_id: int, db: Session = Depends(get_db)):
    return get_payment(db, payment_id)