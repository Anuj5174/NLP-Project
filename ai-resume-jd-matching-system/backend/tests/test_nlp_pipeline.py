"""
Unit tests for the Literature Review NLP pipeline and Custom Edit Distance algorithm.
"""

import os
import sys

# Ensure backend root is on Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.utils.edit_distance import (
    levenshtein_distance,
    damerau_levenshtein_distance,
    edit_similarity,
    get_dp_matrix_and_alignment,
    find_closest_skill,
    fuzzy_match_skills
)
from app.utils.resume_segmenter import (
    segment_resume,
    get_segmented_resume_profile,
    extract_education_details
)
from app.utils.textrank import (
    extract_keywords_textrank,
    summarize_resume_textrank
)
from app.utils.pmi_association import (
    compute_pmi_scores,
    expand_query_skills_with_pmi
)
from app.utils.bm25 import (
    calculate_bm25_single,
    calculate_bm25f_section_weighted
)
from app.utils.fuzzy_similarity import (
    compute_fuzzy_parameterized_similarity
)


def test_edit_distance_basics():
    # 1. Exact match
    assert levenshtein_distance("python", "python") == 0
    assert edit_similarity("python", "python") == 1.0

    # 2. Insertion & Deletion
    assert levenshtein_distance("fast", "fastapi") == 3
    assert levenshtein_distance("fastapi", "fast") == 3

    # 3. Substitution
    assert levenshtein_distance("react", "reach") == 1

    # 4. Transposition (Damerau-Levenshtein)
    # 'teh' -> 'the' is 1 step under Damerau, but 2 steps under pure Levenshtein
    assert damerau_levenshtein_distance("teh", "the") == 1
    assert levenshtein_distance("teh", "the") == 2

    # 5. Typo in technical skill: 'scikitlearn' vs 'scikit-learn'
    assert damerau_levenshtein_distance("scikitlearn", "scikit-learn") == 1
    assert edit_similarity("scikitlearn", "scikit-learn") >= 0.90

    # 6. DP Matrix and Traceback
    align = get_dp_matrix_and_alignment("cat", "hat")
    assert align["distance"] == 1
    assert len(align["dp_matrix"]) == 4
    assert len(align["operations"]) == 3

    # 7. Fuzzy match skills
    resume_skills = ["Pythn", "scikitlearn", "Docker", "PostgreSql"]
    jd_skills = ["Python", "scikit-learn", "Docker", "Kubernetes", "PostgreSQL"]

    res = fuzzy_match_skills(resume_skills, jd_skills)
    assert "Docker" in res["exact_matches"]
    assert "PostgreSQL" in res["exact_matches"] or any(fm["jd_skill"] == "PostgreSQL" for fm in res["fuzzy_matches"])
    assert any(fm["resume_skill"] == "Pythn" and fm["jd_skill"] == "Python" for fm in res["fuzzy_matches"])
    assert any(fm["resume_skill"] == "scikitlearn" and fm["jd_skill"] == "scikit-learn" for fm in res["fuzzy_matches"])
    assert "Kubernetes" in res["missing_skills"]
    print("[PASS] test_edit_distance_basics passed successfully!")


def test_resume_segmentation():
    sample_resume = """
    John Doe
    john@example.com | +91-9876543210
    
    Professional Summary
    Experienced Python Software Engineer with 4 years building APIs.
    
    Technical Skills
    Python, FastAPI, Docker, PostgreSQL, React, AWS
    
    Work Experience
    Senior Developer at TechCorp (2021 - Present)
    Built high-performance microservices and REST APIs using FastAPI and PostgreSQL.
    
    Education
    Bachelor of Technology in Computer Science, IIT Bombay
    """
    profile = get_segmented_resume_profile(sample_resume)
    sections = profile["sections"]

    assert "skills" in sections
    assert "Python" in sections["skills"]
    assert "experience" in sections
    assert "FastAPI" in sections["experience"]
    assert "education" in sections
    assert any("BACHELOR" in deg or "B.TECH" in deg for deg in profile["education_degrees"])
    print("[PASS] test_resume_segmentation passed successfully!")


def test_textrank():
    jd = """
    We are seeking a Senior Python Backend Engineer to build scalable microservices.
    The ideal candidate will have strong experience with Python, FastAPI, Docker, and PostgreSQL.
    You will design REST APIs, optimize database queries, and deploy systems on AWS cloud infrastructure.
    Strong problem solving and communication skills are required.
    """
    keywords = extract_keywords_textrank(jd, max_keywords=5)
    assert len(keywords) > 0
    kw_names = [k["keyword"].lower() for k in keywords]
    print(f"  TextRank Extracted Keywords: {kw_names}")

    resume_text = """
    Experienced software engineer with 5 years in backend development.
    Led the architecture of a high-throughput transaction platform using Python and FastAPI.
    Collaborated with cross-functional product teams to deliver scalable cloud microservices.
    Graduated with Honors in Computer Science.
    """
    summary = summarize_resume_textrank(resume_text, num_sentences=2)
    assert len(summary) > 20
    print(f"  TextRank Summary: {summary}")
    print("[PASS] test_textrank passed successfully!")


def test_pmi_and_bm25_and_fuzzy():
    # PMI expansion
    exp = expand_query_skills_with_pmi(["Python", "React"])
    assert "Python" in exp["expanded_associations"]
    print(f"  PMI Associations for Python: {[a['skill'] for a in exp['expanded_associations']['Python']]}")

    # BM25
    resume = "Experienced Python developer with strong Docker and AWS skills."
    jd = "Looking for a Python developer with Docker skills."
    bm25 = calculate_bm25_single(resume, jd)
    assert bm25["normalized_bm25"] > 0
    print(f"  BM25 Score: {bm25['bm25_score_pct']}%")

    # BM25F
    bm25f = calculate_bm25f_section_weighted(resume, jd)
    assert bm25f["normalized_bm25f"] > 0
    print(f"  BM25F Section-Weighted Score: {bm25f['bm25f_score_pct']}%")

    # Fuzzy Parameterized Similarity
    fuzzy = compute_fuzzy_parameterized_similarity(
        required_jd_skills=["Python", "Docker", "Kubernetes"],
        candidate_skills=["Python", "Docker"],
        resume_text=resume
    )
    assert 0.0 < fuzzy["fuzzy_similarity"] < 1.0
    assert abs(fuzzy["coverage"] - (2 / 3)) < 0.001
    print(f"  Fuzzy Similarity: {fuzzy['fuzzy_score_pct']}% (Coverage: {fuzzy['coverage']}, Strength: {fuzzy['strength']})")
    print("[PASS] test_pmi_and_bm25_and_fuzzy passed successfully!")


if __name__ == "__main__":
    test_edit_distance_basics()
    test_resume_segmentation()
    test_textrank()
    test_pmi_and_bm25_and_fuzzy()
    print("\nALL NLP PIPELINE & EDIT DISTANCE TESTS PASSED!")
