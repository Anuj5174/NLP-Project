"""
Job Description model - stores JDs created by recruiters
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class JobDescription(Base):
    __tablename__ = "job_descriptions"
    
    # Primary key
    jd_id = Column(Integer, primary_key=True, index=True)
    
    # Foreign key to user
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False, index=True)
    
    # Job information
    title = Column(String(255), nullable=False)
    company_name = Column(String(255))
    description = Column(Text, nullable=False)
    
    # Requirements
    required_skills = Column(JSON)  # JSON: list or dict of skills
    experience_required = Column(String(50))  # "0-2 years", "2-5 years", etc.
    location = Column(String(255))
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="job_descriptions")
    matching_results = relationship("MatchingResult", back_populates="job_description", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<JobDescription(title='{self.title}', company='{self.company_name}')>"