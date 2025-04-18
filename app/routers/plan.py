from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.plan import PlanCreate
from app.crud.plan import create_plan, get_plan
from app.database.db import get_db

router = APIRouter(prefix="/plans", tags=["Plans"])

@router.post("/")
def create(plan: PlanCreate, db: Session = Depends(get_db)):
    return create_plan(db, plan)

@router.get("/{plan_id}")
def read(plan_id: int, db: Session = Depends(get_db)):
    return get_plan(db, plan_id)
