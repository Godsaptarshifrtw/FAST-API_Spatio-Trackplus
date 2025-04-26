from sqlalchemy import text
from app.database.session_db import engine, Base
from app.models.session import Session
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_session_db():
    try:
        # Create all tables
        logger.info("Creating session database tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("Session database tables created successfully")
    except Exception as e:
        logger.error(f"Error initializing session database: {str(e)}")
        raise

if __name__ == "__main__":
    init_session_db() 