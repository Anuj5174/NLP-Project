"""
Resume management endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Annotated, Optional
import os
import uuid
from datetime import datetime

from app.utils.skill_extractor import extract_skills_from_text
from app.database import get_db
from app.models.user import User
from app.models.resume import Resume
from app.schemas.resume import ResumeResponse, ResumeList
from app.api.v1.auth import get_current_active_user
from app.utils.pdf_parser import parse_resume
from app.config import settings


router = APIRouter()


def save_upload_file(upload_file: UploadFile, user_id: int) -> str:
    """
    Save uploaded file to disk
    
    Args:
        upload_file: Uploaded file
        user_id: User ID for folder organization
        
    Returns:
        File path where file was saved
    """
    # Create uploads directory if doesn't exist
    upload_dir = settings.UPLOAD_DIR
    os.makedirs(upload_dir, exist_ok=True)
    
    # Generate unique filename
    file_extension = os.path.splitext(upload_file.filename)[1]
    unique_filename = f"{user_id}_{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(upload_dir, unique_filename)
    
    # Save file
    with open(file_path, "wb") as f:
        f.write(upload_file.file.read())
    
    return file_path


@router.post("/upload", response_model=ResumeResponse, status_code=status.HTTP_201_CREATED)
async def upload_resume(
    file: UploadFile = File(..., description="Resume PDF file"),
    candidate_name: Optional[str] = Form(None),
    candidate_email: Optional[str] = Form(None),
    candidate_phone: Optional[str] = Form(None),
    current_user: Annotated[User, Depends(get_current_active_user)] = None,
    db: Session = Depends(get_db)
):
    """
    Upload a resume PDF file
    
    Args:
        file: Resume PDF file
        candidate_name: Optional candidate name
        candidate_email: Optional candidate email
        candidate_phone: Optional candidate phone
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Created resume object
    """
    # Validate file type
    if not file.filename.endswith('.pdf'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are allowed"
        )
    
    # Validate file size (read first to check)
    file_content = await file.read()
    file_size = len(file_content)
    
    if file_size > settings.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File size exceeds maximum allowed size of {settings.MAX_FILE_SIZE / 1024 / 1024}MB"
        )
    
    # Reset file pointer
    await file.seek(0)

    try:
        # Save file
        file_path = save_upload_file(file, current_user.user_id)
        
        # Parse PDF
        parsed_data = parse_resume(file_path)
        
        # Use provided metadata or extracted data
        final_name = candidate_name or parsed_data.get("candidate_name")
        final_email = candidate_email or parsed_data.get("candidate_email")
        final_phone = candidate_phone or parsed_data.get("candidate_phone")
        
        # Extract text and skills
        extracted_text = parsed_data.get("extracted_text", "")
        skills_data = extract_skills_from_text(extracted_text)
        skills_list = [s["skill"] for s in skills_data.get("skills", [])]
        
        # Create resume record
        db_resume = Resume(
            user_id=current_user.user_id,
            candidate_name=final_name,
            candidate_email=final_email,
            candidate_phone=final_phone,
            file_path=file_path,
            file_name=file.filename,
            extracted_text=extracted_text,
            skills_extracted=skills_data,
            uploaded_at=datetime.utcnow()
        )
        
        db.add(db_resume)
        db.commit()
        db.refresh(db_resume)
        
        return ResumeResponse.model_validate(db_resume)
    
    except Exception as e:
        if 'file_path' in locals() and os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing resume: {str(e)}"
        )


@router.get("/", response_model=ResumeList)
async def list_resumes(
    current_user: Annotated[User, Depends(get_current_active_user)] = None,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """
    Get list of all resumes for current user
    
    Args:
        current_user: Current authenticated user
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
        
    Returns:
        List of resumes
    """
    resumes = db.query(Resume).filter(
        Resume.user_id == current_user.user_id
    ).offset(skip).limit(limit).all()
    
    total = db.query(Resume).filter(
        Resume.user_id == current_user.user_id
    ).count()
    
    return {
        "resumes": resumes,
        "total": total
    }


@router.get("/{resume_id}", response_model=ResumeResponse)
async def get_resume(
    resume_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)] = None,
    db: Session = Depends(get_db)
):
    """
    Get a specific resume by ID
    
    Args:
        resume_id: Resume ID
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Resume object
    """
    resume = db.query(Resume).filter(
        Resume.resume_id == resume_id,
        Resume.user_id == current_user.user_id
    ).first()
    
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )
    
    return ResumeResponse.from_orm(resume)


@router.delete("/{resume_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_resume(
    resume_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)] = None,
    db: Session = Depends(get_db)
):
    """
    Delete a resume
    
    Args:
        resume_id: Resume ID
        current_user: Current authenticated user
        db: Database session
    """
    resume = db.query(Resume).filter(
        Resume.resume_id == resume_id,
        Resume.user_id == current_user.user_id
    ).first()
    
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )
    
    # Delete file from disk
    if os.path.exists(resume.file_path):
        os.remove(resume.file_path)
    
    # Delete from database
    db.delete(resume)
    db.commit()
    
    return None