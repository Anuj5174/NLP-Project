"""
matcher.py
─────────────────────────────────────────────────────────────────────────────
Comprehensive Multi-Stage Resume-JD Matching Engine implementing:
  • Paper 1 (Yu et al., 2005): Cascaded resume section segmentation
  • Paper 2 (Mihalcea & Tarau, 2004): Unsupervised TextRank keyword & sentence extraction
  • Paper 3 (Church & Hanks, 1990): Pointwise Mutual Information (PMI) query expansion
  • Paper 4 (Robertson & Zaragoza, 2009): Section-weighted BM25 & BM25F ranking with saturation
  • Paper 5 (Alksasbeh et al., 2021): Fuzzy parameterized set similarity (Coverage + Strength)
  • Our Addition: Sentence-BERT (MiniLM-L6-v2) semantic embeddings
  • Our Custom Edit Distance: Levenshtein / Damerau-Levenshtein typo-tolerant skill matching
─────────────────────────────────────────────────────────────────────────────
"""

from typing import List, Dict, Any, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.utils.semantic_matcher import compute_hybrid_score, semantic_similarity
from app.utils.edit_distance import fuzzy_match_skills, edit_similarity
from app.utils.resume_segmenter import get_segmented_resume_profile, segment_resume
from app.utils.textrank import extract_keywords_textrank, summarize_resume_textrank
from app.utils.pmi_association import expand_query_skills_with_pmi
from app.utils.bm25 import calculate_bm25_single, calculate_bm25f_section_weighted
from app.utils.fuzzy_similarity import compute_fuzzy_parameterized_similarity


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


def calculate_keyword_density(resume_text: str, jd_text: str) -> float:
    """Calculate frequency ratio of JD keywords appearing in the resume."""
    jd_words = set(jd_text.lower().split())
    resume_words = resume_text.lower().split()
    if not resume_words or not jd_words:
        return 0.0
    matches = sum(1 for w in resume_words if w in jd_words)
    return min(matches / len(resume_words) * 10, 1.0)


def match_resume_to_jd(
    resume_text: str,
    jd_text: str,
    resume_skills: List[str],
    jd_required_skills: List[str],
) -> Dict[str, Any]:
    """
    Master matching function executing the 5-paper pipeline + BERT + Custom Edit Distance.
    """
    resume_text = resume_text or ""
    jd_text = jd_text or ""
    resume_skills = resume_skills or []
    jd_required_skills = jd_required_skills or []

    # ══════════════════════════════════════════════════════════════════════════
    # STAGE 1: Cascaded Resume Section Segmentation (Paper 1 — Yu et al.)
    # ══════════════════════════════════════════════════════════════════════════
    resume_profile = get_segmented_resume_profile(resume_text)
    sections = resume_profile["sections"]
    skills_section_text = sections.get("skills", "")
    education_degrees = resume_profile["education_degrees"]
    years_experience = resume_profile["estimated_years_experience"]

    # ══════════════════════════════════════════════════════════════════════════
    # STAGE 2: TextRank Keyword & Sentence Extraction (Paper 2 — Mihalcea & Tarau)
    # ══════════════════════════════════════════════════════════════════════════
    textrank_jd_keywords = extract_keywords_textrank(jd_text, top_fraction=0.33, max_keywords=10)
    resume_executive_summary = summarize_resume_textrank(resume_text, num_sentences=2)

    # ══════════════════════════════════════════════════════════════════════════
    # STAGE 3: PMI Skill Association & Query Expansion (Paper 3 — Church & Hanks)
    # ══════════════════════════════════════════════════════════════════════════
    pmi_expansion = expand_query_skills_with_pmi(
        base_skills=jd_required_skills,
        corpus_text=f"{jd_text}\n{resume_text}",
        max_expansions_per_skill=2
    )

    # ══════════════════════════════════════════════════════════════════════════
    # STAGE 4: Custom Edit Distance Typo-Tolerant Skill Matching
    # ══════════════════════════════════════════════════════════════════════════
    edit_distance_result = fuzzy_match_skills(
        resume_skills=resume_skills,
        jd_skills=jd_required_skills,
        max_distance=2,
        min_similarity=0.80
    )
    all_matched_skills = edit_distance_result["all_matched_skills"]
    missing_skills = edit_distance_result["missing_skills"]
    skill_match_pct = (len(all_matched_skills) / len(jd_required_skills)) if jd_required_skills else 0.0

    # ══════════════════════════════════════════════════════════════════════════
    # STAGE 5: Fuzzy Parameterized Set Similarity (Paper 5 — Alksasbeh et al.)
    # ══════════════════════════════════════════════════════════════════════════
    fuzzy_sim = compute_fuzzy_parameterized_similarity(
        required_jd_skills=jd_required_skills,
        candidate_skills=all_matched_skills,
        resume_text=resume_text,
        skills_section_text=skills_section_text,
        a=0.75,
        b=0.25
    )

    # ══════════════════════════════════════════════════════════════════════════
    # STAGE 6: BM25 & Section-Weighted BM25F Ranking (Paper 4 — Robertson & Zaragoza)
    # ══════════════════════════════════════════════════════════════════════════
    bm25_result = calculate_bm25_single(resume_text, jd_text)
    bm25f_result = calculate_bm25f_section_weighted(resume_text, jd_text)

    # ══════════════════════════════════════════════════════════════════════════
    # STAGE 7: TF-IDF Cosine & Sentence-BERT Embeddings
    # ══════════════════════════════════════════════════════════════════════════
    try:
        vectorizer = TfidfVectorizer(stop_words="english", max_features=5000)
        tfidf_matrix = vectorizer.fit_transform([resume_text, jd_text])
        tfidf_cosine = float(cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])[0][0])
    except Exception:
        tfidf_cosine = 0.0

    keyword_density = calculate_keyword_density(resume_text, jd_text)

    # Compute hybrid text + skill score
    scores = compute_hybrid_score(
        tfidf_cosine=tfidf_cosine,
        skill_match_pct=skill_match_pct,
        keyword_density=keyword_density,
        resume_text=resume_text,
        jd_text=jd_text,
    )

    # Calibrate final score by incorporating BM25F and Fuzzy Strength bonuses
    base_score = scores["final_score"]
    
    # Slight calibrated bonus (up to +5%) if high section-weighted BM25F and fuzzy strength
    calibrated_score = base_score
    if bm25f_result["normalized_bm25f"] > 0.6 and fuzzy_sim["strength"] > 0.8:
        calibrated_score = min(100.0, base_score + 2.0)
    calibrated_score = round(calibrated_score, 2)

    verdict = get_verdict(calibrated_score)

    # ══════════════════════════════════════════════════════════════════════════
    # STAGE 8: Actionable Recommendations
    # ══════════════════════════════════════════════════════════════════════════
    recommendations = []
    if missing_skills:
        recommendations.append(
            f"Candidate is missing core required skills: {', '.join(missing_skills[:5])}."
        )
    if edit_distance_result["fuzzy_matches"]:
        fuzzy_names = [f"{fm['resume_skill']} (~{fm['jd_skill']})" for fm in edit_distance_result["fuzzy_matches"][:3]]
        recommendations.append(
            f"Near skill variations detected via Edit Distance: {', '.join(fuzzy_names)}."
        )
    if skill_match_pct < 0.5:
        recommendations.append(
            "Resume covers less than 50% of required job skills. Significant technical gap."
        )
    if scores["bert_score"] < 0.4:
        recommendations.append(
            "Resume text is not semantically aligned with the JD phrasing. Consider optimizing summary/experience sections."
        )
    if education_degrees:
        recommendations.append(
            f"Recognized academic degree: {', '.join(education_degrees)}."
        )

    return {
        # ── Core Results (Preserves 100% database & test compatibility) ───────
        "match_score":              calibrated_score,
        "verdict":                  verdict,
        "recommendations":          " | ".join(recommendations),

        # ── Classical Scores Breakdown ────────────────────────────────────────
        "cosine_similarity":        scores["tfidf_score"],
        "bert_score":               scores["bert_score"],
        "scoring_method":           scores["scoring_method"],
        "skill_match_percentage":   round(skill_match_pct * 100, 2),
        "keyword_density_score":    scores["keyword_density"],

        # ── Skill Detail ──────────────────────────────────────────────────────
        "matched_skills":           all_matched_skills,
        "missing_skills":           missing_skills,

        # ── Multi-Stage Literature Review & Edit Distance Breakdown ───────────
        "edit_distance_matches":    edit_distance_result["fuzzy_matches"],
        "total_exact_skill_matches": edit_distance_result["total_exact"],
        "total_fuzzy_skill_matches": edit_distance_result["total_fuzzy"],
        "bm25_score":               bm25_result["bm25_score_pct"],
        "bm25f_score":              bm25f_result["bm25f_score_pct"],
        "fuzzy_similarity_score":   fuzzy_sim["fuzzy_score_pct"],
        "fuzzy_coverage":           fuzzy_sim["coverage"],
        "fuzzy_strength":           fuzzy_sim["strength"],
        "textrank_jd_keywords":     [k["keyword"] for k in textrank_jd_keywords],
        "textrank_summary":         resume_executive_summary,
        "pmi_skill_expansions":     pmi_expansion["expanded_associations"],
        "education_degrees":        education_degrees,
        "estimated_years_experience": years_experience,
        "sections_detected":        list(resume_profile["section_word_counts"].keys()),
        "pipeline_stages_applied": [
            "Yu et al. (2005) - Cascaded Section Segmentation",
            "Mihalcea & Tarau (2004) - TextRank Keyword & Executive Summarization",
            "Church & Hanks (1990) - PMI Skill Co-occurrence & Query Expansion",
            "Custom Damerau-Levenshtein Edit Distance (DP Typo Tolerance)",
            "Robertson & Zaragoza (2009) - BM25 & Section-Weighted BM25F Ranking",
            "Alksasbeh et al. (2021) - Fuzzy Parameterized Set Similarity",
            "Sentence-BERT (all-MiniLM-L6-v2) Contextual Embeddings"
        ]
    }
