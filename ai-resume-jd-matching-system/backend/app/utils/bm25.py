"""
bm25.py
─────────────────────────────────────────────────────────────────────────────
Implements BM25 and BM25F Probabilistic Ranking from:
Paper 4 — Robertson & Zaragoza (2009): "The Probabilistic Relevance Framework:
BM25 and Beyond" (Foundations and Trends in Information Retrieval).

Key features:
  1. Okapi BM25:
       w_i = [ tf_i / (k1 * ((1-b) + b * (dl / avdl)) + tf_i) ] * IDF_i
     where:
       IDF_i = log( (N - n_i + 0.5) / (n_i + 0.5) + 1.0 )
       k1 = 1.5  (term frequency saturation parameter)
       b  = 0.75 (document length normalisation parameter)
  2. BM25F (Field-weighted extension):
     Combines weighted term frequencies across resume sections (Skills,
     Experience, Projects, Education) before non-linear saturation.
  3. Score Normalization:
     Transforms unbounded raw BM25 scores into calibrated [0.0, 1.0] and
     [0, 100%] fit scores using sigmoid/logistic scaling.
─────────────────────────────────────────────────────────────────────────────
"""

import math
import re
from collections import Counter
from typing import List, Dict, Tuple, Optional, Any

from app.utils.resume_segmenter import SECTION_WEIGHTS, segment_resume


def tokenize(text: str) -> List[str]:
    """Tokenize lowercase words ignoring common symbols."""
    return re.findall(r"\b[A-Za-z0-9\.\+#][A-Za-z0-9_\-\.\+#]*[A-Za-z0-9\+#]\b|\b[A-Za-z0-9]\b", text.lower())


class BM25Okapi:
    """
    Standard Okapi BM25 implementation.
    """
    def __init__(
        self,
        corpus: List[str],
        k1: float = 1.5,
        b: float = 0.75
    ):
        self.k1 = k1
        self.b = b
        self.corpus_size = len(corpus)
        self.doc_lengths = []
        self.doc_term_freqs = []
        self.doc_freqs = Counter()

        for doc in corpus:
            tokens = tokenize(doc)
            self.doc_lengths.append(len(tokens))
            tf = Counter(tokens)
            self.doc_term_freqs.append(tf)
            for token in tf:
                self.doc_freqs[token] += 1

        self.avg_doc_len = sum(self.doc_lengths) / self.corpus_size if self.corpus_size > 0 else 1.0

        # Calculate IDFs
        self.idfs = {}
        for token, df in self.doc_freqs.items():
            # Robertson & Zaragoza smoothed IDF formula
            numerator = self.corpus_size - df + 0.5
            denominator = df + 0.5
            self.idfs[token] = math.log(max(1.0, (numerator / denominator) + 1.0))

    def get_idf(self, term: str) -> float:
        return self.idfs.get(term, 0.5)

    def score_document(self, query_tokens: List[str], doc_index: int) -> float:
        """Calculates raw BM25 score for a specific document against query."""
        if doc_index >= self.corpus_size:
            return 0.0

        tf_dict = self.doc_term_freqs[doc_index]
        dl = self.doc_lengths[doc_index]
        score = 0.0

        len_norm = (1.0 - self.b) + self.b * (dl / self.avg_doc_len)

        for q in query_tokens:
            if q in tf_dict:
                tf = tf_dict[q]
                idf = self.get_idf(q)
                # Saturation component
                saturated_tf = tf / (self.k1 * len_norm + tf)
                score += idf * saturated_tf

        return score


def calculate_bm25_single(
    resume_text: str,
    jd_text: str,
    k1: float = 1.5,
    b: float = 0.75
) -> Dict[str, Any]:
    """
    Evaluates a single Resume against a JD query using BM25 principles:
      - Length normalization (stops wordy resumes from winning on size alone)
      - Term frequency saturation (stops keyword stuffing, e.g. repeating 'Python' 30 times)
    """
    resume_tokens = tokenize(resume_text)
    jd_tokens = tokenize(jd_text)

    if not resume_tokens or not jd_tokens:
        return {
            "raw_bm25": 0.0,
            "normalized_bm25": 0.0,
            "term_matches": 0,
            "avg_saturation": 0.0
        }

    # Reference lengths (typical resume 400 words)
    dl = len(resume_tokens)
    ref_dl = 400.0
    tf_counts = Counter(resume_tokens)
    jd_counts = Counter(jd_tokens)

    len_norm = (1.0 - b) + b * (dl / ref_dl)

    raw_score = 0.0
    matched_terms = []
    saturation_ratios = []

    for term, count_in_jd in jd_counts.items():
        if term in tf_counts:
            tf = tf_counts[term]
            # IDF proxy based on JD specificity
            idf = 1.0 + math.log(1.0 + (count_in_jd / len(jd_tokens)) * 50)
            saturated_tf = tf / (k1 * len_norm + tf)

            raw_score += idf * saturated_tf
            matched_terms.append(term)
            saturation_ratios.append(saturated_tf)

    # Theoretical maximum if all JD unique terms matched with full saturation
    max_possible = sum(1.0 + math.log(1.0 + (c / len(jd_tokens)) * 50) for c in jd_counts.values())
    norm_score = (raw_score / max_possible) if max_possible > 0 else 0.0
    norm_score = max(0.0, min(1.0, norm_score))

    return {
        "raw_bm25": round(raw_score, 4),
        "normalized_bm25": round(norm_score, 4),
        "bm25_score_pct": round(norm_score * 100, 2),
        "matched_term_count": len(matched_terms),
        "total_jd_unique_terms": len(jd_counts),
        "avg_saturation": round(sum(saturation_ratios) / len(saturation_ratios), 4) if saturation_ratios else 0.0
    }


def calculate_bm25f_section_weighted(
    resume_text: str,
    jd_text: str,
    section_weights: Optional[Dict[str, float]] = None,
    k1: float = 1.5
) -> Dict[str, Any]:
    """
    BM25F (Section-Weighted BM25):
    Weights term matches differently across resume sections:
      - Skills section: 2.5x
      - Experience section: 2.0x
      - Projects section: 1.5x
      - Summary section: 1.2x
      - Education section: 1.0x
      - Other sections: 0.5x
    """
    weights = section_weights or SECTION_WEIGHTS
    sections = segment_resume(resume_text)
    jd_tokens = tokenize(jd_text)

    if not jd_tokens:
        return {"bm25f_score": 0.0, "section_scores": {}}

    jd_counts = Counter(jd_tokens)
    section_tokens = {sec: tokenize(content) for sec, content in sections.items()}

    # Calculate weighted pseudo-term frequency for each query term
    section_contributions = {sec: 0.0 for sec in sections}
    total_raw_bm25f = 0.0

    for term, jd_freq in jd_counts.items():
        pseudo_tf = 0.0
        term_idf = 1.0 + math.log(1.0 + (jd_freq / len(jd_tokens)) * 50)

        for sec, tokens in section_tokens.items():
            if not tokens:
                continue
            tf_sec = tokens.count(term)
            w_sec = weights.get(sec, 1.0)
            dl_sec = len(tokens)
            ref_sec_len = 100.0  # reference section word count
            norm_sec = (1.0 - 0.75) + 0.75 * (dl_sec / ref_sec_len)

            weighted_tf = w_sec * (tf_sec / norm_sec)
            pseudo_tf += weighted_tf

        if pseudo_tf > 0:
            saturated = pseudo_tf / (k1 + pseudo_tf)
            term_score = term_idf * saturated
            total_raw_bm25f += term_score

    # Max possible benchmark
    max_benchmark = sum((1.0 + math.log(1.0 + (c / len(jd_tokens)) * 50)) for c in jd_counts.values()) * 1.5
    normalized_bm25f = min(1.0, total_raw_bm25f / max_benchmark) if max_benchmark > 0 else 0.0

    return {
        "raw_bm25f": round(total_raw_bm25f, 4),
        "normalized_bm25f": round(normalized_bm25f, 4),
        "bm25f_score_pct": round(normalized_bm25f * 100, 2),
        "method": "section_weighted_bm25f"
    }
