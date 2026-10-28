"""
Dashboard Statistics API
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Annotated
from datetime import datetime, timedelta

from app.database import get_db
from app.models.user import User
from app.models.resume import Resume
from app.models.job_description import JobDescription
from app.models.matching_result import MatchingResult
from app.api.v1.auth import get_current_active_user

router = APIRouter()


@router.get("/stats")
async def get_stats(
    current_user: Annotated[User, Depends(get_current_active_user)] = None,
    db: Session = Depends(get_db)
):
    """Get overall dashboard statistics"""

    total_resumes = db.query(Resume).filter(
        Resume.user_id == current_user.user_id
    ).count()

    total_jds = db.query(JobDescription).filter(
        JobDescription.user_id == current_user.user_id
    ).count()

    total_matches = db.query(MatchingResult).join(Resume).filter(
        Resume.user_id == current_user.user_id
    ).count()

    # Average match score
    avg_score = db.query(func.avg(MatchingResult.match_score)).join(Resume).filter(
        Resume.user_id == current_user.user_id
    ).scalar()

    # Verdict breakdown
    highly_recommended = db.query(MatchingResult).join(Resume).filter(
        Resume.user_id == current_user.user_id,
        MatchingResult.verdict == "Highly Recommended"
    ).count()

    recommended = db.query(MatchingResult).join(Resume).filter(
        Resume.user_id == current_user.user_id,
        MatchingResult.verdict == "Recommended"
    ).count()

    consider = db.query(MatchingResult).join(Resume).filter(
        Resume.user_id == current_user.user_id,
        MatchingResult.verdict == "Consider"
    ).count()

    not_recommended = db.query(MatchingResult).join(Resume).filter(
        Resume.user_id == current_user.user_id,
        MatchingResult.verdict == "Not Recommended"
    ).count()

    return {
        "total_resumes": total_resumes,
        "total_job_descriptions": total_jds,
        "total_matches": total_matches,
        "average_match_score": round(float(avg_score or 0), 2),
        "verdict_breakdown": {
            "highly_recommended": highly_recommended,
            "recommended": recommended,
            "consider": consider,
            "not_recommended": not_recommended
        }
    }


@router.get("/recent-matches")
async def get_recent_matches(
    current_user: Annotated[User, Depends(get_current_active_user)] = None,
    db: Session = Depends(get_db),
    limit: int = 10
):
    """Get most recent matching results"""

    results = db.query(MatchingResult).join(Resume).filter(
        Resume.user_id == current_user.user_id
    ).order_by(MatchingResult.created_at.desc()).limit(limit).all()

    return {
        "recent_matches": [
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


@router.get("/top-candidates")
async def get_top_candidates(
    jd_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)] = None,
    db: Session = Depends(get_db),
    limit: int = 10
):
    """Get top candidates for a specific job description"""

    results = db.query(MatchingResult, Resume).join(Resume).filter(
        Resume.user_id == current_user.user_id,
        MatchingResult.jd_id == jd_id
    ).order_by(MatchingResult.match_score.desc()).limit(limit).all()

    return {
        "jd_id": jd_id,
        "top_candidates": [
            {
                "match_id": r.match_id,
                "resume_id": r.resume_id,
                "candidate_name": resume.candidate_name,
                "candidate_email": resume.candidate_email,
                "match_score": r.match_score,
                "verdict": r.verdict,
                "matched_skills": r.matched_skills,
                "missing_skills": r.missing_skills
            }
            for r, resume in results
        ]
    }
