from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()
SESSION_DATABASE_URL = os.getenv("SESSION_DATABASE_URL")

engine = create_engine(SESSION_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_session_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()