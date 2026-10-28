"""
Matching Result model - stores results of resume-JD matching
"""
from sqlalchemy import Column, Integer, Float, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class MatchingResult(Base):
    __tablename__ = "matching_results"
    
    # Primary key
    match_id = Column(Integer, primary_key=True, index=True)
    
    # Foreign keys
    resume_id = Column(Integer, ForeignKey("resumes.resume_id"), nullable=False, index=True)
    jd_id = Column(Integer, ForeignKey("job_descriptions.jd_id"), nullable=False, index=True)
    
    # Matching scores
    match_score = Column(Float, nullable=False)  # 0-100 percentage
    cosine_similarity = Column(Float)  # Raw cosine similarity (0-1)
    skill_match_percentage = Column(Float)  # Percentage of skills matched
    
    # Skill analysis
    matched_skills = Column(JSON)  # JSON: list or dict
    missing_skills = Column(JSON)  # JSON: list or dict
    
    # Verdict
    verdict = Column(String(50))  # "Highly Recommended", "Recommended", etc.
    recommendations = Column(Text)  # Text recommendations for improvement
    
    # Timestamp
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    resume = relationship("Resume", back_populates="matching_results")
    job_description = relationship("JobDescription", back_populates="matching_results")
    
    def __repr__(self):
        return f"<MatchingResult(match_id={self.match_id}, score={self.match_score})>"