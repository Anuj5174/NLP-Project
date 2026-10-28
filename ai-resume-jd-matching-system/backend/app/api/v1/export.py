"""
export.py  —  app/api/v1/export.py
────────────────────────────────────────────────────────────────
Add to your app/api/v1/__init__.py:
    from app.api.v1 import export
    app.include_router(export.router, prefix="/api/v1/export")

Endpoints:
    GET /export/matches/csv?jd_id=1    → Download CSV of all matches for a JD
    GET /export/matches/pdf?jd_id=1    → Download PDF shortlist report for a JD
"""

import csv, io
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.matching_result import MatchingResult
from app.models.resume import Resume
from app.models.job_description import JobDescription

router = APIRouter(tags=["Export"])


# ── Helper: fetch matches for a JD ───────────────────────────────────────────
def _get_matches(jd_id: int, db: Session, user: User):
    jd = db.query(JobDescription).filter(
        JobDescription.jd_id == jd_id,
        JobDescription.user_id == user.user_id
    ).first()
    if not jd:
        raise HTTPException(status_code=404, detail="Job description not found")

    matches = (
        db.query(MatchingResult, Resume)
        .join(Resume, MatchingResult.resume_id == Resume.resume_id)
        .filter(MatchingResult.jd_id == jd_id)
        .order_by(MatchingResult.match_score.desc())
        .all()
    )
    return jd, matches


# ── CSV Export ────────────────────────────────────────────────────────────────
@router.get("/matches/csv")
def export_matches_csv(
    jd_id: int = Query(..., description="Job Description ID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Download a CSV file of all match results for a given JD.
    Sorted by match score descending.
    """
    jd, matches = _get_matches(jd_id, db, current_user)

    output = io.StringIO()
    writer = csv.writer(output)

    # Header row
    writer.writerow([
        "Rank",
        "Candidate Name",
        "Candidate Email",
        "Match Score (%)",
        "Verdict",
        "Skill Match (%)",
        "Matched Skills",
        "Missing Skills",
        "Recommendations",
        "Matched On",
    ])

    for rank, (match, resume) in enumerate(matches, start=1):
        matched = ", ".join(match.matched_skills or [])
        missing = ", ".join(match.missing_skills or [])
        writer.writerow([
            rank,
            resume.candidate_name or "Unknown",
            resume.candidate_email or "N/A",
            round(match.match_score, 2),
            match.verdict,
            round((match.skill_match_percentage or 0), 2),
            matched,
            missing,
            match.recommendations or "",
            match.created_at.strftime("%Y-%m-%d %H:%M") if match.created_at else "",
        ])

    output.seek(0)
    filename = f"shortlist_{jd.title.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.csv"

    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


# ── PDF Export ────────────────────────────────────────────────────────────────
@router.get("/matches/pdf")
def export_matches_pdf(
    jd_id: int = Query(..., description="Job Description ID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Download a formatted PDF shortlist report for a given JD.
    """
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib import colors
        from reportlab.lib.units import mm
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.enums import TA_CENTER
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
        from reportlab.pdfgen import canvas as pdf_canvas
    except ImportError:
        raise HTTPException(status_code=500, detail="reportlab not installed on server.")

    jd, matches = _get_matches(jd_id, db, current_user)

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                            topMargin=15*mm, bottomMargin=15*mm,
                            leftMargin=18*mm, rightMargin=18*mm)

    styles = getSampleStyleSheet()
    BLUE = colors.HexColor("#1a56c4")
    GREEN = colors.HexColor("#10b981")
    RED = colors.HexColor("#ef4444")
    AMBER = colors.HexColor("#f59e0b")

    verdict_colors = {
        "Highly Recommended": GREEN,
        "Recommended": BLUE,
        "Consider": AMBER,
        "Not Recommended": RED,
    }

    story = []

    # Title
    story.append(Paragraph("RecruitAI — Shortlist Report", ParagraphStyle('t',
        fontName='Helvetica-Bold', fontSize=20, textColor=BLUE,
        alignment=TA_CENTER, spaceAfter=2*mm)))
    story.append(Paragraph(f"Job: {jd.title}  |  Company: {jd.company_name or 'N/A'}",
        ParagraphStyle('s', fontName='Helvetica', fontSize=11, textColor=colors.grey,
                       alignment=TA_CENTER, spaceAfter=1*mm)))
    story.append(Paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y %H:%M')}  |  Total Candidates: {len(matches)}",
        ParagraphStyle('d', fontName='Helvetica', fontSize=9, textColor=colors.grey,
                       alignment=TA_CENTER, spaceAfter=4*mm)))
    story.append(HRFlowable(width="100%", thickness=1.5, color=BLUE, spaceAfter=4*mm))

    # Summary stats
    if matches:
        scores = [m.match_score for m, _ in matches]
        avg_score = sum(scores) / len(scores)
        recommended = sum(1 for m, _ in matches if m.verdict in ["Highly Recommended", "Recommended"])
        story.append(Paragraph(
            f"Average Score: <b>{avg_score:.1f}%</b>  |  "
            f"Shortlist Ready: <b>{recommended} candidates</b>  |  "
            f"Top Score: <b>{max(scores):.1f}%</b>",
            ParagraphStyle('stat', fontName='Helvetica', fontSize=10,
                           alignment=TA_CENTER, spaceAfter=4*mm)
        ))

    # Candidate table
    body_style = ParagraphStyle('td', fontName='Helvetica', fontSize=9, leading=12)
    hdr_style = ParagraphStyle('th', fontName='Helvetica-Bold', fontSize=9,
                                textColor=colors.white, leading=12)

    table_data = [[
        Paragraph("#", hdr_style),
        Paragraph("Candidate", hdr_style),
        Paragraph("Score", hdr_style),
        Paragraph("Verdict", hdr_style),
        Paragraph("Matched Skills", hdr_style),
        Paragraph("Missing Skills", hdr_style),
    ]]

    for rank, (match, resume) in enumerate(matches, 1):
        vc = verdict_colors.get(match.verdict, colors.black)
        matched = ", ".join((match.matched_skills or [])[:5])
        missing = ", ".join((match.missing_skills or [])[:3])
        table_data.append([
            Paragraph(str(rank), body_style),
            Paragraph(f"<b>{resume.candidate_name or 'Unknown'}</b><br/>"
                      f"<font color='grey'>{resume.candidate_email or ''}</font>", body_style),
            Paragraph(f"<b>{match.match_score:.1f}%</b>", body_style),
            Paragraph(f'<font color="{vc.hexval()}"><b>{match.verdict}</b></font>', body_style),
            Paragraph(matched or "—", body_style),
            Paragraph(missing or "—", body_style),
        ])

    W = A4[0] - 36*mm
    t = Table(table_data, colWidths=[8*mm, 38*mm, 15*mm, 35*mm, 50*mm, 40*mm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), BLUE),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#f0f4fb")]),
        ('GRID', (0, 0), (-1, -1), 0.4, colors.HexColor("#c8d0e0")),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(t)

    story.append(Spacer(1, 5*mm))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#c8d0e0")))
    story.append(Paragraph("Generated by RecruitAI — AI-Powered Resume & JD Matching System",
        ParagraphStyle('ft', fontName='Helvetica-Oblique', fontSize=8,
                       textColor=colors.grey, alignment=TA_CENTER, spaceAfter=1*mm)))

    def _add_page_number(canvas_obj, doc_obj):
        canvas_obj.setFont('Helvetica', 8)
        canvas_obj.setFillColor(colors.grey)
        page_text = f"Page {canvas_obj.getPageNumber()}"
        canvas_obj.drawRightString(A4[0] - 18*mm, 10*mm, page_text)

    doc.build(story, onFirstPage=_add_page_number, onLaterPages=_add_page_number)
    buffer.seek(0)

    filename = f"shortlist_{jd.title.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.pdf"
    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )
