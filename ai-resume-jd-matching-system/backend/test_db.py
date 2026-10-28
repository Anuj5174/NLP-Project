"""
Test database connection
"""
from sqlalchemy import text, inspect
from app.database import engine

def test_connection():
    """Test connection"""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            print("[OK] Database connection successful!")
            return True
    except Exception as e:
        print(f"[FAIL] Connection failed: {e}")
        return False

def check_tables():
    """Check if tables exist"""
    try:
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        print(f"\nTables in database: {len(tables)}")
        for table in tables:
            print(f"   [OK] {table}")
        
        if len(tables) == 4:
            print("\n[SUCCESS] All 4 tables exist!")
            return True
        else:
            print(f"\n[WARNING] Expected 4 tables, found {len(tables)}")
            return False
    except Exception as e:
        print(f"[ERROR] Error checking tables: {e}")
        return False

if __name__ == "__main__":
    print("Testing database connection...")
    if test_connection():
        check_tables()
        print("\n[OK] Database setup complete!")