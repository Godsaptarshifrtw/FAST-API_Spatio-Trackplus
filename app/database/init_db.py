from sqlalchemy import text
from app.database.db import engine, Base
from app.models.user import User
from app.models.plan import Plan
from app.models.payment import Payment
from app.models.subscription import Subscription
from app.models.device import Device
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db():
    try:
        # Create all tables
        logger.info("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")

        # Add password_hash column if it doesn't exist
        with engine.connect() as conn:
            # Check if password_hash column exists
            result = conn.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='users' AND column_name='password_hash';
            """))
            if not result.fetchone():
                logger.info("Adding password_hash column to users table...")
                conn.execute(text("""
                    ALTER TABLE users 
                    ADD COLUMN password_hash VARCHAR(200) NOT NULL DEFAULT '';
                """))
                conn.commit()
                logger.info("password_hash column added successfully")

    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")
        raise

if __name__ == "__main__":
    init_db() 