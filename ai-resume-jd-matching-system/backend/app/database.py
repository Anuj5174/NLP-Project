"""
Database connection and session management using SQLAlchemy
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

# Create database engine (supports both PostgreSQL and SQLite)
if settings.DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        settings.DATABASE_URL,
        connect_args={"check_same_thread": False},
        echo=settings.DEBUG
    )
else:
    engine = create_engine(
        settings.DATABASE_URL,
        pool_pre_ping=True,  # Check connection before using
        pool_size=10,         # Number of connections to maintain
        max_overflow=20,      # Max extra connections beyond pool_size
        echo=settings.DEBUG   # Log SQL queries in debug mode
    )

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for all models
Base = declarative_base()

def get_db():
    """
    Dependency function to get database session
    Use in FastAPI endpoints: db: Session = Depends(get_db)
    Automatically closes session after request
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initialize database - create all tables"""
    from app.models import user, resume, job_description, matching_result
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully!")