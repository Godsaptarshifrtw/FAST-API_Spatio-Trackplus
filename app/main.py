from fastapi import FastAPI
from app.routers import user, device, subscription, plan, payment, session
from app.database.customer_db import Base, engine
from app.database.session_db import SessionBase, session_engine
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Create all tables in both databases (run once at startup)
Base.metadata.create_all(bind=engine)  # Main DB
SessionBase.metadata.create_all(bind=session_engine)  # Session DB

app = FastAPI(
    title="Subscription and Device Management API",
    version="1.0.0",
    description="Backend system to manage users, subscriptions, devices, sessions, and payments."
)

# Include Routers
app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(device.router, prefix="/devices", tags=["Devices"])
app.include_router(subscription.router, prefix="/subscriptions", tags=["Subscriptions"])
app.include_router(plan.router, prefix="/plans", tags=["Plans"])
app.include_router(payment.router, prefix="/payments", tags=["Payments"])
app.include_router(session.router, prefix="/sessions", tags=["Sessions"])
