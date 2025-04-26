import sys
import os
from pathlib import Path

# Add the project root to the Python path
project_root = str(Path(__file__).parent.parent.parent)
sys.path.append(project_root)

from app.database.migrations.add_password_hash import upgrade, downgrade

def run_migrations():
    try:
        print("Starting database migrations...")
        upgrade()
        print("Migrations completed successfully!")
    except Exception as e:
        print(f"Error running migrations: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    run_migrations() 