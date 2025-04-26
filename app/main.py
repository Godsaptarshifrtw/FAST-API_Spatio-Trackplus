from fastapi import FastAPI
from app.routers import user, device, subscription, plan, payment, session
from app.database.db import Base, engine
from app.database.session_db import Base as SessionBase, engine as session_engine
from app.models.user import User
from app.models.plan import Plan
from app.models.payment import Payment
from app.models.subscription import Subscription
from app.models.device import Device
from app.models.session import Session
from dotenv import load_dotenv
import logging
from app.database.init_db import init_db
from app.database.init_session_db import init_session_db

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env
load_dotenv()

# Initialize databases
logger.info("Initializing databases...")
init_db()
init_session_db()
logger.info("Database initialization completed")

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
