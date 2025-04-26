from sqlalchemy import Column, String, text
from app.database.db import Base, engine
from app.models.user import User

def upgrade():
    # Add the password_hash column
    with engine.connect() as conn:
        # First check if the column exists
        result = conn.execute(text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='users' AND column_name='password_hash';
        """))
        if not result.fetchone():
            # Column doesn't exist, add it
            conn.execute(text("""
                ALTER TABLE users 
                ADD COLUMN password_hash VARCHAR(200) NOT NULL DEFAULT '';
            """))
            conn.commit()
            print("Added password_hash column to users table")

def downgrade():
    with engine.connect() as conn:
        # Check if the column exists before trying to drop it
        result = conn.execute(text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='users' AND column_name='password_hash';
        """))
        if result.fetchone():
            # Column exists, drop it
            conn.execute(text("""
                ALTER TABLE users 
                DROP COLUMN password_hash;
            """))
            conn.commit()
            print("Dropped password_hash column from users table") 