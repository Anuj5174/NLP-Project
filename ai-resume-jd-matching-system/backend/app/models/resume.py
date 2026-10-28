"""
Resume model - stores uploaded resumes and extracted data
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Resume(Base):
    __tablename__ = "resumes"
    
    # Primary key
    resume_id = Column(Integer, primary_key=True, index=True)
    
    # Foreign key to user
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False, index=True)
    
    # Candidate information (extracted from resume)
    candidate_name = Column(String(255))
    candidate_email = Column(String(255))
    candidate_phone = Column(String(50))
    
    # File information
    file_path = Column(String(500))
    file_name = Column(String(255))
    
    # Extracted content
    extracted_text = Column(Text)  # Full text from PDF
    skills_extracted = Column(JSON)  # JSON: list or dict of skills
    
    # Metadata
    total_experience_years = Column(Integer)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="resumes")
    matching_results = relationship("MatchingResult", back_populates="resume", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Resume(candidate='{self.candidate_name}', file='{self.file_name}')>"