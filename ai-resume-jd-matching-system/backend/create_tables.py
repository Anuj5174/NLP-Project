"""
Force create all database tables
"""
from app.database import Base, engine
from app.models.user import User
from app.models.resume import Resume
from app.models.job_description import JobDescription
from app.models.matching_result import MatchingResult

def create_all_tables():
    """Create all tables"""
    print("Creating tables...")
    print(f"Models loaded: User, Resume, JobDescription, MatchingResult")
    
    # This will create all tables
    Base.metadata.create_all(bind=engine)
    
    print("[OK] Tables created successfully!")
    
    # Verify tables exist
    from sqlalchemy import inspect
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    
    print(f"\nTables in database: {tables}")
    
    if len(tables) == 4:
        print("\n[OK] SUCCESS! All 4 tables created!")
    else:
        print(f"\n[WARNING]: Expected 4 tables, found {len(tables)}")

if __name__ == "__main__":
    create_all_tables()