"""
matcher.py
─────────────────────────────────────────────────────────────────────────────
Resume-to-JD Matching Engine built on:
"Competence-Level Prediction and Resume & Job Description Matching
Using Context-Aware Transformer Models"
Changmao Li et al. (EMNLP 2020).

Key Architectural Components:
  • 6-Section Hierarchical Resume Segmentation
  • Section-Aware Chunking (§4.1.3)
  • Learned Section Encodings: h_{i,j}^{final} = h_{i,j}^{chunk} + e_i^{section}
  • Bidirectional Cross-Document Multi-Head Attention (R2B & B2R)
  • Dynamic Candidate Scoring & Requirement Evidence Attribution
─────────────────────────────────────────────────────────────────────────────
"""

from typing import List, Dict, Any, Optional
from app.utils.context_aware_transformer import match_context_aware_transformer


def get_verdict(score: float) -> str:
    """Classify final match score into standard recruiter verdict categories."""
    if score >= 75.0:
        return "Highly Recommended"
    elif score >= 60.0:
        return "Recommended"
    elif score >= 50.0:
        return "Consider"
    else:
        return "Not Recommended"


def match_resume_to_jd(
    resume_text: str,
    jd_text: str,
    resume_skills: Optional[List[str]] = None,
    jd_required_skills: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Executes the EMNLP 2020 Context-Aware Transformer Matching Architecture.
    """
    resume_text = resume_text or ""
    jd_text = jd_text or ""

    # Defensive normalization of skills
    if isinstance(resume_skills, dict):
        resume_skills = [s["skill"] for s in resume_skills.get("skills", []) if isinstance(s, dict) and "skill" in s]
    elif isinstance(resume_skills, list):
        resume_skills = [s if isinstance(s, str) else s.get("skill", "") for s in resume_skills if s and s != "null"]
    else:
        resume_skills = []
    if not resume_skills and resume_text:
        from app.utils.skill_extractor import get_skill_names_only
        resume_skills = get_skill_names_only(resume_text)

    if isinstance(jd_required_skills, list):
        jd_required_skills = [s for s in jd_required_skills if isinstance(s, str) and s.lower() != "null"]
    else:
        jd_required_skills = []
    if not jd_required_skills and jd_text:
        from app.utils.skill_extractor import get_skill_names_only
        jd_required_skills = get_skill_names_only(jd_text)

    # Execute Context-Aware Transformer pipeline
    result = match_context_aware_transformer(
        resume_text=resume_text,
        jd_text=jd_text,
        resume_skills=resume_skills,
        jd_required_skills=jd_required_skills
    )

    # Return full structured result ensuring 100% database & API compatibility
    return {
        # ── Core Results ──────────────────────────────────────────────────────
        "match_score":              result["match_score"],
        "verdict":                  result["verdict"],
        "recommendations":          result["recommendations"],

        # ── Classical Scores Breakdown ────────────────────────────────────────
        "cosine_similarity":        result["cosine_similarity"],
        "bert_score":               result["bert_score"],
        "scoring_method":           "context_aware_transformer_emnlp2020",
        "skill_match_percentage":   result["skill_match_percentage"],
        "keyword_density_score":    round(result["section_scores"]["skills"] / 100.0, 2),

        # ── Skill Detail ──────────────────────────────────────────────────────
        "matched_skills":           result["matched_skills"],
        "missing_skills":           result["missing_skills"],

        # ── RecruitAI Evidence-Aware Score Breakdown ─────────────────────────
        "score_breakdown":          result.get("score_breakdown"),
        "matched_requirements":     result["matched_requirements"],
        "missing_evidence":         result["missing_evidence"],
        "section_scores":           result["section_scores"],
        "total_chunks_analyzed":    result["total_chunks_analyzed"],
        "architecture":             result["architecture"],
        "pipeline_stages_applied":  result["pipeline_stages_applied"],

    }
