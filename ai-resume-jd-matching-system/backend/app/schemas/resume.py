"""
Resume schemas for validation
"""
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from datetime import datetime
from typing import Union, List


class ResumeUpload(BaseModel):
    """Schema for resume upload"""
    candidate_name: Optional[str] = None
    candidate_email: Optional[EmailStr] = None
    candidate_phone: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "candidate_name": "John Doe",
                "candidate_email": "john@example.com",
                "candidate_phone": "+91-1234567890"
            }
        }


class ResumeResponse(BaseModel):
    resume_id: int
    user_id: int
    candidate_name: Optional[str] = None
    candidate_email: Optional[str] = None
    candidate_phone: Optional[str] = None
    file_name: str
    file_path: str
    extracted_text: Optional[str] = None
    skills_extracted: Optional[Union[List[str], dict]] = None# ← ADD THIS LINE
    uploaded_at: datetime
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "resume_id": 1,
                "user_id": 1,
                "candidate_name": "John Doe",
                "candidate_email": "john@example.com",
                "candidate_phone": "+91-1234567890",
                "file_name": "john_doe_resume.pdf",
                "file_path": "uploads/resume_1.pdf",
                "extracted_text": "John Doe\nSoftware Engineer...",
                "uploaded_at": "2026-03-08T10:00:00"
            }
        }


class ResumeList(BaseModel):
    resumes: list[ResumeResponse]
    total: int
    
    class Config:
        from_attributes = True