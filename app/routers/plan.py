from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database.db import get_db
from app.schemas.plan import PlanCreate, Plan, PlanUpdate
from app.models.plan import Plan as PlanModel
from app.models.user import User as UserModel
from app.auth.auth import get_current_user
from datetime import datetime
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/", response_model=Plan)
def create_plan(plan: PlanCreate, 
                db: Session = Depends(get_db),
                current_user: UserModel = Depends(get_current_user)):
    # Create new plan
    db_plan = PlanModel(
        name=plan.name,
        description=plan.description,
        price=plan.price,
        duration_days=plan.duration_days,
        max_devices=plan.max_devices,
        features=plan.features,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(db_plan)
    db.commit()
    db.refresh(db_plan)
    return db_plan

@router.get("/{plan_id}", response_model=Plan)
def get_plan(plan_id: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching plan with ID: {plan_id}")
    db_plan = db.query(PlanModel).filter(PlanModel.plan_id == plan_id).first()
    if db_plan is None:
        logger.warning(f"Plan not found with ID: {plan_id}")
        raise HTTPException(status_code=404, detail="Plan not found")
    return db_plan

@router.get("/", response_model=List[Plan])
def get_plans(active_only: bool = True, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    logger.info(f"Fetching plans with active_only={active_only}, skip={skip}, limit={limit}")
    query = db.query(PlanModel)
    if active_only:
        query = query.filter(PlanModel.is_active == True)
    plans = query.offset(skip).limit(limit).all()
    logger.info(f"Found {len(plans)} plans")
    return plans

@router.put("/{plan_id}", response_model=Plan)
def update_plan(plan_id: int, 
                plan: PlanUpdate, 
                db: Session = Depends(get_db),
                current_user: UserModel = Depends(get_current_user)):
    db_plan = db.query(PlanModel).filter(PlanModel.plan_id == plan_id).first()
    if db_plan is None:
        raise HTTPException(status_code=404, detail="Plan not found")
    
    update_data = plan.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_plan, key, value)
    
    db_plan.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_plan)
    return db_plan

@router.delete("/{plan_id}")
def delete_plan(plan_id: int, 
                db: Session = Depends(get_db),
                current_user: UserModel = Depends(get_current_user)):
    db_plan = db.query(PlanModel).filter(PlanModel.plan_id == plan_id).first()
    if db_plan is None:
        raise HTTPException(status_code=404, detail="Plan not found")
    
    db.delete(db_plan)
    db.commit()
    return {"message": "Plan deleted successfully"}