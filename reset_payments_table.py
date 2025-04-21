from app.database.db import Base, engine
from app.models.payment import Payment
from app.models.user import User
from app.models.plan import Plan
from sqlalchemy import text

def reset_tables():
    # Drop all tables
    with engine.connect() as conn:
        conn.execute(text("DROP TABLE IF EXISTS payments CASCADE"))
        conn.execute(text("DROP TABLE IF EXISTS subscriptions CASCADE"))
        conn.execute(text("DROP TABLE IF EXISTS plans CASCADE"))
        conn.execute(text("DROP TABLE IF EXISTS users CASCADE"))
        conn.commit()
    
    # Create all tables in the correct order
    Base.metadata.create_all(engine)
    print("All tables have been reset successfully!")

if __name__ == "__main__":
    reset_tables() 