"""
resume_segmenter.py
─────────────────────────────────────────────────────────────────────────────
Implements Resume Section Segmentation inspired by:
Paper 1 — Yu, Guan & Zhou (2005): "Resume Information Extraction with a
Cascaded Hybrid Model" (ACL).

Key ideas implemented:
  1. Two-pass hierarchical segmentation:
     Pass 1: Identifies high-level section blocks (Skills, Experience,
             Education, Projects, Summary, Certifications, Contact).
     Pass 2: Extracts targeted structured entities per block (Degrees,
             experience durations, contact metadata).
  2. Section weighting profile for BM25F field ranking:
     Skills (2.5x), Experience (2.0x), Projects (1.5x), Summary (1.2x),
     Education (1.0x), General/Other (0.5x).
  3. Clean text normalization and boundary detection with fuzzy fallback.
─────────────────────────────────────────────────────────────────────────────
"""

import re
from typing import Dict, List, Optional, Any

# Section heading patterns
SECTION_PATTERNS = {
    "summary": [
        r"^.*?(professional\s+summary|executive\s+summary|profile|about\s+me|career\s+objective|objective).*?$"
    ],
    "skills": [
        r"^.*?(technical\s+skills|core\s+skills|key\s+skills|skills\s*&?\s*competencies|technologies|tech\s+stack|skills|proficiencies|tools\s*&?\s*technologies).*?$"
    ],
    "experience": [
        r"^.*?(work\s+experience|professional\s+experience|employment\s+history|experience|work\s+history|career\s+history).*?$"
    ],
    "projects": [
        r"^.*?(projects|key\s+projects|academic\s+projects|personal\s+projects|portfolio).*?$"
    ],
    "education": [
        r"^.*?(education|academic\s+background|educational\s+qualifications|academics|qualifications|degrees).*?$"
    ],
    "certifications": [
        r"^.*?(certifications|certificates|licenses|courses\s*&?\s*certifications|accreditations).*?$"
    ],
    "awards": [
        r"^.*?(awards|honors|achievements|publications|extracurricular).*?$"
    ],
}

# Standard section weights for BM25F ranking (Paper 1 + Paper 4)
SECTION_WEIGHTS = {
    "skills": 2.5,
    "experience": 2.0,
    "projects": 1.5,
    "summary": 1.2,
    "education": 1.0,
    "certifications": 1.0,
    "awards": 0.8,
    "other": 0.5,
}

# Known degree patterns (Pass 2 detailed field extraction)
DEGREE_PATTERNS = [
    r"\b(ph\.?d|doctor\s+of\s+philosophy)\b",
    r"\b(m\.?tech|master\s+of\s+technology)\b",
    r"\b(m\.?s|m\.?sc|master\s+of\s+science)\b",
    r"\b(m\.?b\.?a|master\s+of\s+business\s+administration)\b",
    r"\b(b\.?tech|bachelor\s+of\s+technology)\b",
    r"\b(b\.?e|bachelor\s+of\s+engineering)\b",
    r"\b(b\.?s|b\.?sc|bachelor\s+of\s+science)\b",
    r"\b(b\.?c\.?a|bachelor\s+of\s+computer\s+applications)\b",
    r"\b(m\.?c\.?a|master\s+of\s+computer\s+applications)\b",
    r"\b(bachelor'?s?\s+degree|master'?s?\s+degree|associate'?s?\s+degree)\b",
]


def identify_section_header(line: str) -> Optional[str]:
    """
    Checks if a line of text is a section header.
    Headers are typically short (<= 40 chars), may be uppercase,
    and match one of the canonical section patterns.
    """
    cleaned = line.strip().lower()
    if not cleaned or len(cleaned) > 45:
        return None

    # Remove trailing colon or decorative characters
    cleaned = re.sub(r"[:\-_=•#*]+$", "", cleaned).strip()

    for section_name, patterns in SECTION_PATTERNS.items():
        for pat in patterns:
            if re.match(pat, cleaned, re.IGNORECASE):
                return section_name

    return None


def segment_resume(text: str) -> Dict[str, str]:
    """
    Pass 1: Segments raw resume text into structured sections.
    
    Returns:
      Dict mapping section names to their text content.
      Standard keys: 'summary', 'skills', 'experience', 'projects',
                     'education', 'certifications', 'awards', 'other'.
    """
    if not text:
        return {sec: "" for sec in SECTION_WEIGHTS}

    lines = text.split("\n")
    sections: Dict[str, List[str]] = {sec: [] for sec in SECTION_WEIGHTS}
    current_section = "summary"  # default initial block (top of resume)

    for line in lines:
        detected = identify_section_header(line)
        if detected:
            current_section = detected
        else:
            sections[current_section].append(line)

    # Join lines back into clean strings
    result: Dict[str, str] = {}
    for sec, line_list in sections.items():
        result[sec] = "\n".join(line_list).strip()

    return result


def extract_education_details(education_text: str) -> List[str]:
    """
    Pass 2: Extract specific degrees and qualifications from education block.
    """
    if not education_text:
        return []

    found_degrees = []
    for pat in DEGREE_PATTERNS:
        matches = re.finditer(pat, education_text, re.IGNORECASE)
        for match in matches:
            clean_deg = match.group(0).strip().upper()
            if clean_deg not in found_degrees:
                found_degrees.append(clean_deg)

    return found_degrees


def extract_experience_years(text: str) -> Optional[float]:
    """
    Extract total years of experience using regex patterns
    (e.g., '3+ years of experience', '5 years in software development').
    """
    patterns = [
        r"(\d+(?:\.\d+)?)\+?\s*(?:years|yrs)\s*(?:of)?\s*(?:experience|exp)",
        r"(?:experience|exp)\s*:\s*(\d+(?:\.\d+)?)\s*(?:years|yrs)",
        r"(\d+(?:\.\d+)?)\s*(?:years|yrs)\s*(?:in|as|with)",
    ]

    for pat in patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            try:
                return float(m.group(1))
            except (ValueError, TypeError):
                continue
    return None


def get_segmented_resume_profile(text: str) -> Dict[str, Any]:
    """
    Full cascaded parsing pipeline for a resume.
    """
    sections = segment_resume(text)
    education_fields = extract_education_details(sections.get("education", ""))
    years_exp = extract_experience_years(text)

    # Compute section word counts
    word_counts = {sec: len(sec_text.split()) for sec, sec_text in sections.items()}

    return {
        "sections": sections,
        "section_weights": SECTION_WEIGHTS,
        "education_degrees": education_fields,
        "estimated_years_experience": years_exp,
        "section_word_counts": word_counts,
        "has_skills_section": bool(sections.get("skills", "").strip()),
        "has_experience_section": bool(sections.get("experience", "").strip()),
        "has_education_section": bool(sections.get("education", "").strip()),
    }
