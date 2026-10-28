"""
User model - stores user account information
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"
    
    # Primary key
    user_id = Column(Integer, primary_key=True, index=True)
    
    # User credentials
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    
    # User information
    full_name = Column(String(255))
    role = Column(String(50), default="recruiter")  # recruiter or admin
    
    # Account status
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships (one user can have many resumes, JDs)
    resumes = relationship("Resume", back_populates="user", cascade="all, delete-orphan")
    job_descriptions = relationship("JobDescription", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(email='{self.email}', name='{self.full_name}')>"