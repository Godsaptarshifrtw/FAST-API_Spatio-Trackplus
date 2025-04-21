from fastapi import FastAPI
from app.routers import user, device, subscription, plan, payment, session
from app.database.db import Base, engine
from app.database.session_db import Base as SessionBase, engine as session_engine
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env
load_dotenv()

# Create all tables in both databases (run once at startup)
logger.info("Creating database tables...")
Base.metadata.create_all(bind=engine)  # Main DB
logger.info("Main database tables created")
SessionBase.metadata.create_all(bind=session_engine)  # Session DB
logger.info("Session database tables created")

app = FastAPI(
    title="Subscription and Device Management API",
    version="1.0.0",
    description="Backend system to manage users, subscriptions, devices, sessions, and payments."
)

# Include Routers
logger.info("Registering routers...")
app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(device.router, prefix="/devices", tags=["Devices"])
app.include_router(subscription.router, prefix="/subscriptions", tags=["Subscriptions"])
app.include_router(plan.router, prefix="/plans", tags=["Plans"])
app.include_router(payment.router, prefix="/payments", tags=["Payments"])
app.include_router(session.router, prefix="/sessions", tags=["Sessions"])
logger.info("All routers registered")
