"""
shortlist.py  —  app/api/v1/shortlist.py
────────────────────────────────────────────────────────────────
Add to app/api/v1/__init__.py:
    from app.api.v1 import shortlist
    app.include_router(shortlist.router, prefix="/api/v1/shortlist")

Endpoints:
    POST /shortlist/email          → Send emails to selected candidates
    POST /shortlist/email/single   → Send email to one candidate
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.matching_result import MatchingResult
from app.models.resume import Resume
from app.models.job_description import JobDescription
from app.utils.email_service import send_shortlist_email

router = APIRouter(tags=["Shortlist & Email"])


# ── Request schemas ───────────────────────────────────────────────────────────
class BulkEmailRequest(BaseModel):
    match_ids: List[int]           # list of match_id values to email
    custom_message: Optional[str] = ""
    subject: Optional[str] = None


class SingleEmailRequest(BaseModel):
    match_id: int
    custom_message: Optional[str] = ""
    subject: Optional[str] = None


# ── Bulk Email: send to multiple shortlisted candidates ───────────────────────
@router.post("/email")
def send_bulk_shortlist_emails(
    payload: BulkEmailRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Send shortlist emails to multiple candidates at once.
    Called from the Bulk Match results page when recruiter
    selects candidates and clicks 'Email Shortlisted'.

    Request body:
    {
      "match_ids": [1, 3, 5],
      "custom_message": "We'd love to schedule a call with you this week.",
      "subject": "Interview Invitation — Python Developer"
    }
    """
    results = []

    for match_id in payload.match_ids:
        result = _send_one(
            match_id=match_id,
            custom_message=payload.custom_message,
            subject=payload.subject,
            db=db,
            recruiter_name=current_user.full_name or "The Recruiter",
        )
        results.append(result)

    sent_count    = sum(1 for r in results if r.get("success"))
    failed_count  = len(results) - sent_count

    return {
        "total": len(results),
        "sent": sent_count,
        "failed": failed_count,
        "results": results,
    }


# ── Single Email ──────────────────────────────────────────────────────────────
@router.post("/email/single")
def send_single_shortlist_email(
    payload: SingleEmailRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Send a shortlist email to one candidate.
    Called from the individual Match Result page.

    Request body:
    {
      "match_id": 7,
      "custom_message": "Please bring your portfolio to the interview.",
      "subject": "Interview Invitation — Data Scientist"
    }
    """
    result = _send_one(
        match_id=payload.match_id,
        custom_message=payload.custom_message,
        subject=payload.subject,
        db=db,
        recruiter_name=current_user.full_name or "The Recruiter",
    )
    if not result.get("success"):
        raise HTTPException(status_code=500, detail=result.get("error", "Failed to send email"))
    return result


# ── Internal helper ───────────────────────────────────────────────────────────
def _send_one(match_id: int, custom_message: str, subject: Optional[str],
              db: Session, recruiter_name: str) -> dict:
    match = db.query(MatchingResult).filter(MatchingResult.match_id == match_id).first()
    if not match:
        return {"match_id": match_id, "success": False, "error": "Match not found"}

    resume = db.query(Resume).filter(Resume.resume_id == match.resume_id).first()
    jd     = db.query(JobDescription).filter(JobDescription.jd_id == match.jd_id).first()

    if not resume or not resume.candidate_email:
        return {
            "match_id": match_id,
            "success": False,
            "error": f"No email found for candidate {resume.candidate_name if resume else 'Unknown'}"
        }

    result = send_shortlist_email(
        to_email=resume.candidate_email,
        candidate_name=resume.candidate_name or "Candidate",
        job_title=jd.title if jd else "the position",
        company_name=jd.company_name if jd else "",
        match_score=match.match_score,
        verdict=match.verdict,
        matched_skills=match.matched_skills or [],
        custom_message=custom_message or "",
        recruiter_name=recruiter_name,
        subject=subject,
    )

    result["match_id"]       = match_id
    result["candidate_name"] = resume.candidate_name
    result["candidate_email"] = resume.candidate_email
    return result
