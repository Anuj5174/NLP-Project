"""
email_service.py  —  app/utils/email_service.py
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
from app.config import settings


# ── Email template ────────────────────────────────────────────────────────────
def build_email_html(
    candidate_name: str,
    job_title: str,
    company_name: str,
    match_score: float,
    verdict: str,
    matched_skills: list,
    custom_message: str,
    recruiter_name: str,
) -> str:
    skills_html = "".join(
        f'<span style="background:#e8f5e9;color:#2e7d32;padding:3px 10px;'
        f'border-radius:12px;margin:3px;display:inline-block;font-size:13px;">{s}</span>'
        for s in matched_skills[:8]
    )
    verdict_color = {
        "Highly Recommended": "#10b981",
        "Recommended": "#1a56c4",
        "Consider": "#f59e0b",
        "Not Recommended": "#ef4444",
    }.get(verdict, "#1a56c4")

    return f"""
<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body style="font-family: 'Segoe UI', Arial, sans-serif; background:#f5f7fa; margin:0; padding:20px;">
  <div style="max-width:600px; margin:0 auto; background:white; border-radius:12px;
               box-shadow:0 4px 20px rgba(0,0,0,0.08); overflow:hidden;">
    <div style="background:#1a56c4; padding:28px 32px; text-align:center;">
      <h1 style="color:white; margin:0; font-size:24px; letter-spacing:1px;">RecruitAI</h1>
      <p style="color:#a8d4ff; margin:6px 0 0; font-size:13px;">AI-Powered Recruitment Intelligence</p>
    </div>
    <div style="padding:32px;">
      <p style="color:#333; font-size:16px; margin-top:0;">Dear <b>{candidate_name}</b>,</p>
      <p style="color:#444; line-height:1.7;">
        We reviewed your application for the <b>{job_title}</b> position
        {f'at <b>{company_name}</b>' if company_name else ''}.
        Our AI system has evaluated your profile and we are pleased to share the following:
      </p>
      <div style="background:#f0f4fb; border-radius:10px; padding:20px; text-align:center; margin:20px 0;">
        <p style="margin:0; color:#666; font-size:13px; text-transform:uppercase; letter-spacing:1px;">Your Match Score</p>
        <p style="margin:8px 0; font-size:42px; font-weight:bold; color:#1a56c4;">{match_score:.1f}%</p>
        <span style="background:{verdict_color}; color:white; padding:5px 18px;
                     border-radius:20px; font-size:13px; font-weight:bold;">{verdict}</span>
      </div>
      <p style="color:#333; font-weight:bold; margin-bottom:8px;">✅ Skills Matched:</p>
      <div style="margin-bottom:20px;">{skills_html if skills_html else '<em style="color:#888">Skills data unavailable</em>'}</div>
      {'<div style="background:#e8f0fe;border-left:4px solid #1a56c4;padding:14px 18px;border-radius:0 8px 8px 0;margin:20px 0;">'
        + f'<p style="margin:0;color:#1a56c4;font-weight:bold;">Message from {recruiter_name}:</p>'
        + f'<p style="margin:8px 0 0;color:#333;line-height:1.6;">{custom_message}</p>'
        + '</div>' if custom_message else ''}
      <p style="color:#444; line-height:1.7;">
        We look forward to the possibility of working with you.
        Please reply to this email to confirm your interest or ask any questions.
      </p>
      <p style="color:#333;">
        Best regards,<br>
        <b>{recruiter_name}</b><br>
        <span style="color:#888; font-size:13px;">Sent via RecruitAI</span>
      </p>
    </div>
    <div style="background:#f8f9fa; padding:16px 32px; text-align:center; border-top:1px solid #e9ecef;">
      <p style="margin:0; color:#aaa; font-size:11px;">
        This email was sent by RecruitAI — AI-Powered Resume & JD Matching System.
      </p>
    </div>
  </div>
</body>
</html>
"""


# ── Method 1: Gmail SMTP ──────────────────────────────────────────────────────
def send_via_gmail(to_email: str, subject: str, html_body: str) -> dict:
    gmail_user = settings.GMAIL_USER
    gmail_pass = settings.GMAIL_APP_PASSWORD.replace(" ", "")

    if not gmail_user or not gmail_pass:
        return {"success": False, "error": "Gmail credentials not set in .env"}

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"]    = f"RecruitAI <{gmail_user}>"
        msg["To"]      = to_email
        msg.attach(MIMEText(html_body, "html"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(gmail_user, gmail_pass)
            server.sendmail(gmail_user, to_email, msg.as_string())

        return {"success": True, "method": "gmail", "to": to_email}
    except Exception as e:
        return {"success": False, "error": str(e), "method": "gmail"}


# ── Method 2: SendGrid ────────────────────────────────────────────────────────
def send_via_sendgrid(to_email: str, to_name: str, subject: str, html_body: str) -> dict:
    try:
        import sendgrid
        from sendgrid.helpers.mail import Mail
    except ImportError:
        return {"success": False, "error": "sendgrid package not installed."}

    api_key    = settings.SENDGRID_API_KEY
    from_email = settings.SENDGRID_FROM_EMAIL
    from_name  = settings.SENDGRID_FROM_NAME

    if not api_key or not from_email:
        return {"success": False, "error": "SendGrid credentials not set in .env"}

    try:
        sg = sendgrid.SendGridAPIClient(api_key=api_key)
        message = Mail(
            from_email=(from_email, from_name),
            to_emails=(to_email, to_name),
            subject=subject,
            html_content=html_body,
        )
        response = sg.send(message)
        return {
            "success": response.status_code in [200, 201, 202],
            "method": "sendgrid",
            "status_code": response.status_code,
            "to": to_email,
        }
    except Exception as e:
        return {"success": False, "error": str(e), "method": "sendgrid"}


# ── Unified send function ─────────────────────────────────────────────────────
def send_shortlist_email(
    to_email: str,
    candidate_name: str,
    job_title: str,
    company_name: str,
    match_score: float,
    verdict: str,
    matched_skills: list,
    custom_message: str,
    recruiter_name: str,
    subject: Optional[str] = None,
) -> dict:
    html    = build_email_html(
        candidate_name=candidate_name,
        job_title=job_title,
        company_name=company_name,
        match_score=match_score,
        verdict=verdict,
        matched_skills=matched_skills,
        custom_message=custom_message,
        recruiter_name=recruiter_name,
    )
    subject = subject or f"Interview Invitation — {job_title} at {company_name or 'Our Company'}"
    method  = settings.EMAIL_METHOD.lower()

    if method == "sendgrid":
        return send_via_sendgrid(to_email, candidate_name, subject, html)
    else:
        return send_via_gmail(to_email, subject, html)