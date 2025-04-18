from fastapi import FastAPI
from app.routers import user, device, subscription, plan, payment, session
from app.database.db import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user.router)
app.include_router(device.router)
app.include_router(subscription.router)
app.include_router(plan.router)
app.include_router(payment.router)
app.include_router(session.router)