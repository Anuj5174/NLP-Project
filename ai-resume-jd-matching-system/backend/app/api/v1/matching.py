"""
Matching API endpoints - Resume to JD matching
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated
from datetime import datetime

from app.database import get_db
from app.models.user import User
from app.models.resume import Resume
from app.models.job_description import JobDescription
from app.models.matching_result import MatchingResult
from app.api.v1.auth import get_current_active_user
from app.utils.matcher import match_resume_to_jd

router = APIRouter()


@router.post("/single")
async def match_single(
    resume_id: int,
    jd_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)] = None,
    db: Session = Depends(get_db)
):
    """Match a single resume against a job description"""

    resume = db.query(Resume).filter(
        Resume.resume_id == resume_id,
        Resume.user_id == current_user.user_id
    ).first()

    if not resume:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found")

    jd = db.query(JobDescription).filter(
        JobDescription.jd_id == jd_id,
        JobDescription.user_id == current_user.user_id
    ).first()

    if not jd:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job description not found")

    # Run matching algorithm with skills
    result = match_resume_to_jd(
        resume_text=resume.extracted_text or "",
        jd_text=jd.description or "",
        resume_skills=resume.skills_extracted or [],
        jd_required_skills=jd.required_skills or []
    )

    # Save result to database
    db_result = MatchingResult(
        resume_id=resume_id,
        jd_id=jd_id,
        match_score=result["match_score"],
        cosine_similarity=result["cosine_similarity"],
        skill_match_percentage=result["skill_match_percentage"],
        matched_skills=result["matched_skills"],
        missing_skills=result["missing_skills"],
        verdict=result["verdict"],
        recommendations=result["recommendations"],
        created_at=datetime.utcnow()
    )

    db.add(db_result)
    db.commit()
    db.refresh(db_result)

    return {
        "match_id": db_result.match_id,
        "resume_id": resume_id,
        "jd_id": jd_id,
        "candidate_name": resume.candidate_name,
        "jd_title": jd.title,
        **result
    }


@router.post("/bulk")
async def match_bulk(
    jd_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)] = None,
    db: Session = Depends(get_db)
):
    """Match ALL resumes against a single job description"""

    jd = db.query(JobDescription).filter(
        JobDescription.jd_id == jd_id,
        JobDescription.user_id == current_user.user_id
    ).first()

    if not jd:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job description not found")

    resumes = db.query(Resume).filter(
        Resume.user_id == current_user.user_id
    ).all()

    if not resumes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No resumes found")

    results = []

    for resume in resumes:
        # Run matching algorithm with skills
        result = match_resume_to_jd(
            resume_text=resume.extracted_text or "",
            jd_text=jd.description or "",
            resume_skills=resume.skills_extracted or [],
            jd_required_skills=jd.required_skills or []
        )

        db_result = MatchingResult(
            resume_id=resume.resume_id,
            jd_id=jd_id,
            match_score=result["match_score"],
            cosine_similarity=result["cosine_similarity"],
            skill_match_percentage=result["skill_match_percentage"],
            matched_skills=result["matched_skills"],
            missing_skills=result["missing_skills"],
            verdict=result["verdict"],
            recommendations=result["recommendations"],
            created_at=datetime.utcnow()
        )

        db.add(db_result)
        db.commit()
        db.refresh(db_result)

        results.append({
            "match_id": db_result.match_id,
            "resume_id": resume.resume_id,
            "candidate_name": resume.candidate_name,
            "match_score": result["match_score"],
            "verdict": result["verdict"],
            "matched_skills": result["matched_skills"],
            "missing_skills": result["missing_skills"]
        })

    results.sort(key=lambda x: x["match_score"], reverse=True)

    return {
        "jd_id": jd_id,
        "jd_title": jd.title,
        "total_resumes": len(results),
        "results": results
    }


@router.get("/results")
async def get_match_results(
    current_user: Annotated[User, Depends(get_current_active_user)] = None,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 50
):
    """Get all matching results for current user"""

    results = db.query(MatchingResult).join(Resume).filter(
        Resume.user_id == current_user.user_id
    ).offset(skip).limit(limit).all()

    return {
        "total": len(results),
        "results": [
            {
                "match_id": r.match_id,
                "resume_id": r.resume_id,
                "jd_id": r.jd_id,
                "match_score": r.match_score,
                "verdict": r.verdict,
                "created_at": str(r.created_at)
            }
            for r in results
        ]
    }