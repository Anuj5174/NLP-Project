"""
Skill Extractor - Extract skills from resume text using NLP
"""
import re
try:
    import spacy
    try:
        nlp = spacy.load("en_core_web_sm")
    except OSError:
        nlp = None
except ImportError:
    spacy = None
    nlp = None

from typing import Optional
from app.utils.skills_database import (
    SKILLS_DATABASE,
    SKILL_SYNONYMS,
    get_all_skills,
    get_skill_category,
    normalize_skill
)


def preprocess_text(text: str) -> str:
    """
    Clean and preprocess text before skill extraction
    """
    if not text:
        return ""
    
    # Lowercase
    text = text.lower()
    
    # Replace common separators with spaces
    text = re.sub(r'[•\-|/\\,;]', ' ', text)
    
    # Remove special characters but keep dots (for node.js, react.js etc)
    text = re.sub(r'[^\w\s\.]', ' ', text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text


def extract_skills_from_text(text: str) -> dict:
    """
    Main function - Extract skills from resume text
    
    Args:
        text: Raw resume text
        
    Returns:
        Dictionary with extracted skills, categories and confidence scores
    """
    if not text:
        return {
            "skills": [],
            "skills_by_category": {},
            "total_skills_found": 0
        }

    cleaned_text = preprocess_text(text)
    all_skills = get_all_skills()
    
    found_skills = {}  # skill -> confidence score

    # --- Method 1: Direct string matching (most reliable) ---
    for skill in all_skills:
        skill_lower = skill.lower()
        # Use word boundary matching to avoid partial matches
        pattern = r'\b' + re.escape(skill_lower) + r'\b'
        if re.search(pattern, cleaned_text):
            normalized = normalize_skill(skill_lower)
            if normalized not in found_skills:
                found_skills[normalized] = 0.9  # high confidence for exact match

    # --- Method 2: spaCy NLP token matching ---
    if nlp:
        doc = nlp(cleaned_text[:10000])  # limit text size for performance
        
        for token in doc:
            token_text = token.text.lower()
            normalized = normalize_skill(token_text)
            
            if normalized in [normalize_skill(s) for s in all_skills]:
                if normalized not in found_skills:
                    found_skills[normalized] = 0.8  # slightly lower confidence

        # Check noun chunks (multi-word skills like "machine learning")
        for chunk in doc.noun_chunks:
            chunk_text = chunk.text.lower().strip()
            normalized = normalize_skill(chunk_text)
            
            if chunk_text in all_skills or normalized in all_skills:
                if normalized not in found_skills:
                    found_skills[normalized] = 0.85

    # --- Method 3: Synonym matching ---
    for synonym, standard in SKILL_SYNONYMS.items():
        pattern = r'\b' + re.escape(synonym) + r'\b'
        if re.search(pattern, cleaned_text):
            if standard not in found_skills:
                found_skills[standard] = 0.85

    # --- Organize by category ---
    skills_by_category = {}
    skills_list = []
    
    for skill, confidence in found_skills.items():
        category = get_skill_category(skill)
        
        if category not in skills_by_category:
            skills_by_category[category] = []
        
        skill_obj = {
            "skill": skill,
            "category": category,
            "confidence": round(confidence, 2)
        }
        
        skills_by_category[category].append(skill_obj)
        skills_list.append(skill_obj)

    # Sort by confidence
    skills_list.sort(key=lambda x: x["confidence"], reverse=True)

    return {
        "skills": skills_list,
        "skills_by_category": skills_by_category,
        "total_skills_found": len(skills_list)
    }


def get_skill_names_only(text: str) -> list[str]:
    """
    Returns just the skill names as a simple list
    Useful for quick comparisons
    """
    result = extract_skills_from_text(text)
    return [s["skill"] for s in result["skills"]]


def compare_skills(resume_text: str, jd_text: str) -> dict:
    """
    Compare skills between resume and job description
    
    Args:
        resume_text: Resume text
        jd_text: Job description text
        
    Returns:
        Dict with matched, missing skills and percentage
    """
    resume_skills = set(get_skill_names_only(resume_text))
    jd_skills = set(get_skill_names_only(jd_text))
    
    matched = resume_skills.intersection(jd_skills)
    missing = jd_skills - resume_skills
    extra = resume_skills - jd_skills  # skills in resume but not in JD
    
    match_percentage = (
        round((len(matched) / len(jd_skills)) * 100, 2)
        if jd_skills else 0
    )
    
    return {
        "matched_skills": list(matched),
        "missing_skills": list(missing),
        "extra_skills": list(extra),
        "skill_match_percentage": match_percentage,
        "total_jd_skills": len(jd_skills),
        "total_resume_skills": len(resume_skills),
        "total_matched": len(matched)
    }
