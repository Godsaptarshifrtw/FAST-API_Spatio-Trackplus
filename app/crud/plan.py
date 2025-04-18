from sqlalchemy.orm import Session
from app.models.plan import Plan
from app.schemas.plan import PlanCreate

def create_plan(db: Session, plan: PlanCreate):
    db_plan = Plan(**plan.dict())
    db.add(db_plan)
    db.commit()
    db.refresh(db_plan)
    return db_plan

def get_plan(db: Session, plan_id: int):
    return db.query(Plan).filter(Plan.plan_id == plan_id).first()