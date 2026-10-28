"""
semantic_matcher.py
────────────────────────────────────────────────────────────────
Drop-in upgrade for matcher.py
Uses sentence-transformers (BERT) for SEMANTIC similarity on top
of TF-IDF. Two resumes can use completely different words but mean
the same thing — BERT catches that, TF-IDF doesn't.

Install once:
    pip install sentence-transformers

Model downloads automatically on first run (~90 MB, cached after).
"""

from functools import lru_cache
from typing import Optional

# ── lazy import so the server still starts if not installed ──────────────────
try:
    from sentence_transformers import SentenceTransformer, util as st_util
    SBERT_AVAILABLE = True
except ImportError:
    SBERT_AVAILABLE = False


# ── singleton model (loads once, reused for every request) ───────────────────
@lru_cache(maxsize=1)
def _get_model() -> Optional["SentenceTransformer"]:
    """Load the model once and cache it in memory."""
    if not SBERT_AVAILABLE:
        return None
    # all-MiniLM-L6-v2  →  fast, small (80 MB), great accuracy
    # all-mpnet-base-v2 →  slower, larger, marginally better (swap if you want)
    return SentenceTransformer("all-MiniLM-L6-v2")


def semantic_similarity(text1: str, text2: str) -> float:
    """
    Returns a float 0.0 – 1.0 representing the SEMANTIC similarity
    between two text documents using BERT sentence embeddings.

    Falls back to 0.0 gracefully if sentence-transformers is not installed.

    Example
    -------
    score = semantic_similarity(resume_text, jd_text)
    # score = 0.81  →  highly related
    """
    model = _get_model()
    if model is None or not text1.strip() or not text2.strip():
        return 0.0

    embeddings = model.encode([text1, text2], convert_to_tensor=True)
    score = st_util.cos_sim(embeddings[0], embeddings[1])
    return float(score.item())


# ════════════════════════════════════════════════════════════════════════════
# UPDATED SCORING FORMULA  (paste this into your matcher.py)
# ════════════════════════════════════════════════════════════════════════════
"""
OLD formula (TF-IDF only):
    final_score = (0.60 * cosine_sim) + (0.30 * skill_match) + (0.10 * keyword_density)

NEW formula (TF-IDF + BERT hybrid):
    tfidf_score    = cosine similarity from TF-IDF vectors
    bert_score     = semantic_similarity(resume_text, jd_text)
    text_score     = (0.40 * tfidf_score) + (0.60 * bert_score)   ← BERT weighted higher
    final_score    = (0.60 * text_score)  + (0.30 * skill_match)  + (0.10 * keyword_density)

Why this weighting?
  • BERT captures meaning even when words differ  ("developer" ≈ "engineer")
  • TF-IDF catches exact keyword overlap, still useful for technical terms
  • Skill match remains the strongest single recruiter signal
  • Tested on 20 resume-JD pairs — see test_accuracy.py for results
"""


def compute_hybrid_score(
    tfidf_cosine: float,
    skill_match_pct: float,
    keyword_density: float,
    resume_text: str,
    jd_text: str,
) -> dict:
    """
    Computes the full hybrid match score combining TF-IDF + BERT + Skill Match.

    Parameters
    ----------
    tfidf_cosine    : float  — cosine similarity from your existing TF-IDF code (0–1)
    skill_match_pct : float  — % of JD skills found in resume (0–1)
    keyword_density : float  — keyword frequency score (0–1)
    resume_text     : str    — full extracted resume text
    jd_text         : str    — full job description text

    Returns
    -------
    dict with keys:
        tfidf_score     : float
        bert_score      : float
        text_score      : float
        skill_match_pct : float
        keyword_density : float
        final_score     : float  (0–100, percentage)
        scoring_method  : str    ("hybrid" or "tfidf_only")
    """
    bert_score = semantic_similarity(resume_text, jd_text)

    if SBERT_AVAILABLE and bert_score > 0:
        # Hybrid: BERT weighted higher than TF-IDF within the text component
        text_score = (0.40 * tfidf_cosine) + (0.60 * bert_score)
        method = "hybrid_bert_tfidf"
    else:
        # Fallback: pure TF-IDF (original behavior)
        text_score = tfidf_cosine
        method = "tfidf_only"

    final_score = (
        (0.60 * text_score) +
        (0.30 * skill_match_pct) +
        (0.10 * keyword_density)
    ) * 100  # convert to 0–100

    return {
        "tfidf_score":      round(tfidf_cosine, 4),
        "bert_score":       round(bert_score, 4),
        "text_score":       round(text_score, 4),
        "skill_match_pct":  round(skill_match_pct, 4),
        "keyword_density":  round(keyword_density, 4),
        "final_score":      round(min(final_score, 100.0), 2),
        "scoring_method":   method,
    }
