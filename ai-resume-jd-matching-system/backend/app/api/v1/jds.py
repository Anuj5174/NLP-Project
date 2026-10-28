"""
Job Description management endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated, Optional
from datetime import datetime

from app.database import get_db
from app.models.user import User
from app.models.job_description import JobDescription
from app.api.v1.auth import get_current_active_user
from pydantic import BaseModel

router = APIRouter()


# -------------------------
# Schemas (inline for simplicity)
# -------------------------

class JDCreate(BaseModel):
    title: str
    company_name: Optional[str] = None
    description: str
    required_skills: Optional[list] = None
    experience_required: Optional[str] = None
    location: Optional[str] = None

    class Config:
        from_attributes = True


class JDResponse(BaseModel):
    jd_id: int
    user_id: int
    title: str
    company_name: Optional[str] = None
    description: str
    required_skills: Optional[list] = None
    experience_required: Optional[str] = None
    location: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


# -------------------------
# Routes
# -------------------------

@router.post("/", response_model=JDResponse, status_code=status.HTTP_201_CREATED)
async def create_jd(
    jd_data: JDCreate,
    current_user: Annotated[User, Depends(get_current_active_user)] = None,
    db: Session = Depends(get_db)
):
    """Create a new job description"""
    db_jd = JobDescription(
        user_id=current_user.user_id,
        title=jd_data.title,
        company_name=jd_data.company_name,
        description=jd_data.description,
        required_skills=jd_data.required_skills,
        experience_required=jd_data.experience_required,
        location=jd_data.location,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    db.add(db_jd)
    db.commit()
    db.refresh(db_jd)

    return JDResponse.model_validate(db_jd)


@router.get("/", response_model=list[JDResponse])
async def list_jds(
    current_user: Annotated[User, Depends(get_current_active_user)] = None,
    db: Session = Depends(get_db)
):
    """Get all job descriptions for current user"""
    jds = db.query(JobDescription).filter(
        JobDescription.user_id == current_user.user_id
    ).all()

    return [JDResponse.model_validate(jd) for jd in jds]


@router.get("/{jd_id}", response_model=JDResponse)
async def get_jd(
    jd_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)] = None,
    db: Session = Depends(get_db)
):
    """Get a specific job description"""
    jd = db.query(JobDescription).filter(
        JobDescription.jd_id == jd_id,
        JobDescription.user_id == current_user.user_id
    ).first()

    if not jd:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job description not found"
        )

    return JDResponse.model_validate(jd)


@router.delete("/{jd_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_jd(
    jd_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)] = None,
    db: Session = Depends(get_db)
):
    """Delete a job description"""
    jd = db.query(JobDescription).filter(
        JobDescription.jd_id == jd_id,
        JobDescription.user_id == current_user.user_id
    ).first()

    if not jd:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job description not found"
        )

    db.delete(jd)
    db.commit()

    return None
