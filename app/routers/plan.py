from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.db import get_db
from app.schemas.plan import PlanCreate, Plan, PlanUpdate
from app.models.plan import Plan as PlanModel
from datetime import datetime
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/", response_model=Plan)
def create_plan(plan: PlanCreate, db: Session = Depends(get_db)):
    logger.info(f"Creating new plan: {plan.model_dump()}")
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
    logger.info(f"Plan created successfully with ID: {db_plan.plan_id}")
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
def update_plan(plan_id: int, plan: PlanUpdate, db: Session = Depends(get_db)):
    logger.info(f"Updating plan with ID: {plan_id}")
    db_plan = db.query(PlanModel).filter(PlanModel.plan_id == plan_id).first()
    if db_plan is None:
        logger.warning(f"Plan not found with ID: {plan_id}")
        raise HTTPException(status_code=404, detail="Plan not found")
    
    update_data = plan.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_plan, key, value)
    
    db.commit()
    db.refresh(db_plan)
    logger.info(f"Plan {plan_id} updated successfully")
    return db_plan

@router.delete("/{plan_id}")
def delete_plan(plan_id: int, db: Session = Depends(get_db)):
    logger.info(f"Deleting plan with ID: {plan_id}")
    db_plan = db.query(PlanModel).filter(PlanModel.plan_id == plan_id).first()
    if db_plan is None:
        logger.warning(f"Plan not found with ID: {plan_id}")
        raise HTTPException(status_code=404, detail="Plan not found")
    
    db.delete(db_plan)
    db.commit()
    logger.info(f"Plan {plan_id} deleted successfully")
    return {"message": "Plan deleted successfully"}