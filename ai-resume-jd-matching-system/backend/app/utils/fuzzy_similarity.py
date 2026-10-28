"""
fuzzy_similarity.py
─────────────────────────────────────────────────────────────────────────────
Implements Fuzzy Parameterized Set Similarity from:
Paper 5 — Alksasbeh et al. (2021): "Smart Job Searching System Based on
Information Retrieval and Fuzzy Parameterized Sets" (IJECE).

Key features:
  1. Graded partial credit instead of all-or-nothing binary filtering.
  2. Two-tier evaluation:
       S = a * Coverage + b * Strength,  where a = 0.75, b = 0.25, a + b = 1
  3. Coverage component:
       Coverage = |A ∩ B| / |A|
     where A is required JD skills and B is candidate resume skills.
  4. Strength / Proficiency component (corrects the inversion flaw identified
     in Alksasbeh et al.):
       Strength = (1 / |A ∩ B|) * sum_{e in A ∩ B} [ 1 - |μ_job(e) - μ_cv(e)| ]
     where μ_cv(e) ∈ [0.0, 1.0] reflects the candidate's depth and prominence
     for skill e (e.g., mentioned in skills section vs once in body).
  5. Dynamic Matched & Missing skill sets (A ∩ B and A - B).
─────────────────────────────────────────────────────────────────────────────
"""

from typing import List, Dict, Set, Optional, Any


def compute_skill_membership(
    skill: str,
    resume_text: str,
    skills_section_text: str = ""
) -> float:
    """
    Computes fuzzy membership grade μ_cv(e) in range [0.2, 1.0]:
      - If skill appears in designated 'Skills' section: high base (0.8)
      - Bonus for frequency across project & experience sections (+0.1 to +0.2)
      - Casual single mention in body: 0.5
    """
    s_low = skill.lower()
    text_low = resume_text.lower()
    skills_sec_low = skills_section_text.lower() if skills_section_text else ""

    occurrences = text_low.count(s_low)
    if occurrences == 0:
        return 0.0

    in_skills_section = s_low in skills_sec_low

    if in_skills_section:
        grade = 0.80 + min(0.20, (occurrences - 1) * 0.05)
    else:
        grade = 0.50 + min(0.35, occurrences * 0.10)

    return round(min(1.0, grade), 3)


def compute_fuzzy_parameterized_similarity(
    required_jd_skills: List[str],
    candidate_skills: List[str],
    resume_text: str = "",
    skills_section_text: str = "",
    a: float = 0.75,
    b: float = 0.25,
    default_job_grade: float = 1.0
) -> Dict[str, Any]:
    """
    Computes Alksasbeh et al. (2021) fuzzy parameterized set similarity.
    
    Formula:
      S = a * (|A ∩ B| / |A|) + b * [ (1 / |A ∩ B|) * sum_{e in A ∩ B} (1 - |μ_job - μ_cv|) ]
    """
    a_set = {s.lower().strip() for s in required_jd_skills if s and s.strip()}
    b_set = {s.lower().strip() for s in candidate_skills if s and s.strip()}

    if not a_set:
        return {
            "fuzzy_similarity": 1.0,
            "fuzzy_score_pct": 100.0,
            "coverage": 1.0,
            "strength": 1.0,
            "matched_skills": list(b_set),
            "missing_skills": [],
            "skill_grades": {}
        }

    intersection = a_set & b_set
    missing = a_set - b_set

    # 1. Coverage
    coverage = len(intersection) / len(a_set)

    # 2. Strength / Closeness
    skill_grades: Dict[str, Dict[str, float]] = {}
    closeness_sum = 0.0

    for skill in intersection:
        mu_cv = compute_skill_membership(skill, resume_text, skills_section_text)
        mu_job = default_job_grade
        gap = abs(mu_job - mu_cv)
        closeness = 1.0 - gap

        closeness_sum += closeness
        skill_grades[skill] = {
            "mu_job": mu_job,
            "mu_cv": mu_cv,
            "closeness": round(closeness, 3)
        }

    strength = (closeness_sum / len(intersection)) if intersection else 0.0

    # 3. Combined similarity
    # If no skills intersect, strength is 0
    final_similarity = (a * coverage) + (b * strength)
    final_similarity = max(0.0, min(1.0, final_similarity))

    return {
        "fuzzy_similarity": round(final_similarity, 4),
        "fuzzy_score_pct": round(final_similarity * 100, 2),
        "coverage": round(coverage, 4),
        "strength": round(strength, 4),
        "coverage_weight": a,
        "strength_weight": b,
        "matched_skills": list(intersection),
        "missing_skills": list(missing),
        "skill_grades": skill_grades,
        "total_required": len(a_set),
        "total_matched": len(intersection)
    }
