from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.db import get_db
from app.schemas.plan import PlanCreate, Plan
from app.models.plan import Plan as PlanModel
from datetime import datetime

router = APIRouter()

@router.post("/", response_model=Plan)
def create_plan(plan: PlanCreate, db: Session = Depends(get_db)):
    db_plan = PlanModel(
        product_id=plan.product_id,
        name=plan.name,
        price=plan.price,
        duration_days=plan.duration_days,
        features=plan.features,
        is_active=plan.is_active,
        created_at=datetime.utcnow()
    )
    db.add(db_plan)
    db.commit()
    db.refresh(db_plan)
    return db_plan

@router.get("/{plan_id}", response_model=Plan)
def get_plan(plan_id: int, db: Session = Depends(get_db)):
    db_plan = db.query(PlanModel).filter(PlanModel.plan_id == plan_id).first()
    if db_plan is None:
        raise HTTPException(status_code=404, detail="Plan not found")
    return db_plan

@router.get("/", response_model=List[Plan])
def get_plans(active_only: bool = True, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    query = db.query(PlanModel)
    if active_only:
        query = query.filter(PlanModel.is_active == True)
    plans = query.offset(skip).limit(limit).all()
    return plans
