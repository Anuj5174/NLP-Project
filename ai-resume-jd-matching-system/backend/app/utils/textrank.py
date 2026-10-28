"""
textrank.py
─────────────────────────────────────────────────────────────────────────────
Implements TextRank Keyword and Sentence Extraction from:
Paper 2 — Mihalcea & Tarau (2004): "TextRank: Bringing Order into Texts" (EMNLP).

Key features:
  1. Keyword TextRank:
     - Part-of-speech filtering: Nouns and Adjectives (NN*, JJ*).
     - Co-occurrence graph with sliding window size N = 2 (undirected).
     - Weighted PageRank formula with damping factor d = 0.85.
     - Phrase formation: Adjacent top-ranked words merged into multi-word
       technical requirements (e.g., 'machine learning', 'REST API').
  2. Sentence TextRank:
     - Sentence graph weighted by shared word similarity:
       Weight(Si, Sj) = |words(Si) ∩ words(Sj)| / (log(len(Si)) + log(len(Sj)))
     - Generates 2-3 line executive summaries of candidate resumes.
  3. No external dependency on spacy required (uses standard NLTK or pure-python fallback).
─────────────────────────────────────────────────────────────────────────────
"""

import math
import re
from typing import List, Dict, Tuple, Set, Optional, Any

# Stopwords set
DEFAULT_STOPWORDS = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are",
    "aren't", "as", "at", "be", "because", "been", "before", "being", "below", "between", "both",
    "but", "by", "can", "can't", "cannot", "could", "couldn't", "did", "didn't", "do", "does",
    "doesn't", "doing", "don't", "down", "during", "each", "few", "for", "from", "further", "had",
    "hadn't", "has", "hasn't", "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her",
    "here", "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd",
    "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's", "its", "itself",
    "let's", "me", "more", "most", "mustn't", "my", "myself", "no", "nor", "not", "of", "off",
    "on", "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own",
    "same", "shan't", "she", "she'd", "she'll", "she's", "should", "shouldn't", "so", "some",
    "such", "than", "that", "that's", "the", "their", "theirs", "them", "themselves", "then",
    "there", "there's", "these", "they", "they'd", "they'll", "they're", "they've", "this",
    "those", "through", "to", "too", "under", "until", "up", "very", "was", "wasn't", "we", "we'd",
    "we'll", "we're", "we've", "were", "weren't", "what", "what's", "when", "when's", "where",
    "where's", "which", "while", "who", "who's", "whom", "why", "why's", "with", "won't", "would",
    "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself",
    "yourselves", "will", "shall", "must", "experience", "required", "responsible", "looking"
}

# Try importing nltk pos_tag
try:
    import nltk
    from nltk.tokenize import sent_tokenize, word_tokenize
    from nltk import pos_tag
    NLTK_AVAILABLE = True
except Exception:
    NLTK_AVAILABLE = False


def _tokenize_words(text: str) -> List[str]:
    """Tokenize words and preserve alphanumeric + technical terms."""
    return re.findall(r"\b[A-Za-z0-9][A-Za-z0-9_\-\.\+#]*[A-Za-z0-9\+#]\b|\b[A-Za-z0-9]\b", text)


def _split_sentences(text: str) -> List[str]:
    """Split text into sentences cleanly."""
    if NLTK_AVAILABLE:
        try:
            return [s.strip() for s in sent_tokenize(text) if s.strip()]
        except Exception:
            pass
    # Regex fallback
    raw_sents = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9])", text)
    cleaned = []
    for s in raw_sents:
        s_clean = s.strip()
        if len(s_clean) > 15:
            cleaned.append(s_clean)
    return cleaned


def _is_noun_or_adjective(word: str, tag: Optional[str] = None) -> bool:
    """Filter to nouns and adjectives as proven optimal in Mihalcea & Tarau (2004)."""
    if word.lower() in DEFAULT_STOPWORDS or len(word) < 2:
        return False
    if tag:
        return tag.startswith("NN") or tag.startswith("JJ")
    # Heuristic fallback if POS tagger not loaded:
    # Reject common verbs/adverbs, accept alphanumeric nouns
    return not word.lower().endswith("ly") and not word.isdigit()


def pagerank_graph(
    adjacency_matrix: Dict[Any, Dict[Any, float]],
    nodes: List[Any],
    d: float = 0.85,
    max_iter: int = 40,
    tol: float = 0.0001
) -> Dict[Any, float]:
    """
    Computes PageRank over an arbitrary weighted graph.
    Formula:
      WS(Vi) = (1 - d) + d * sum_{Vj in In(Vi)} [ (w_{ji} / sum_{Vk in Out(Vj)} w_{jk}) * WS(Vj) ]
    """
    n = len(nodes)
    if n == 0:
        return {}

    # Initialize scores uniformly
    scores = {node: 1.0 for node in nodes}

    # Precalculate sum of outgoing weights for each node
    out_sums = {}
    for u in nodes:
        out_sums[u] = sum(adjacency_matrix.get(u, {}).values())

    for _ in range(max_iter):
        new_scores = {}
        max_diff = 0.0

        for vi in nodes:
            incoming_sum = 0.0
            for vj in nodes:
                if vi in adjacency_matrix.get(vj, {}):
                    w_ji = adjacency_matrix[vj][vi]
                    w_out = out_sums.get(vj, 0.0)
                    if w_out > 0:
                        incoming_sum += (w_ji / w_out) * scores[vj]

            new_scores[vi] = (1.0 - d) + d * incoming_sum
            diff = abs(new_scores[vi] - scores[vi])
            if diff > max_diff:
                max_diff = diff

        scores = new_scores
        if max_diff < tol:
            break

    return scores


def extract_keywords_textrank(
    text: str,
    top_fraction: float = 0.33,
    window_size: int = 2,
    max_keywords: int = 15
) -> List[Dict[str, Any]]:
    """
    Extracts key phrases from Job Description / Resume using TextRank algorithm.

    Steps:
      1. Tokenize and filter tokens to nouns and adjectives.
      2. Build undirected co-occurrence graph with window N = 2.
      3. Run PageRank (d = 0.85).
      4. Retain top 1/3 vertices.
      5. Post-processing: Merge adjacent high-ranking words into phrases.
    """
    if not text:
        return []

    tokens = _tokenize_words(text)
    if not tokens:
        return []

    # Part of speech tagging
    tagged_tokens: List[Tuple[str, str]] = []
    if NLTK_AVAILABLE:
        try:
            tagged_tokens = pos_tag(tokens)
        except Exception:
            tagged_tokens = [(t, "NN") for t in tokens]
    else:
        tagged_tokens = [(t, "NN") for t in tokens]

    # Filtered candidate words
    valid_words = []
    word_indices = []
    for idx, (tok, tag) in enumerate(tagged_tokens):
        if _is_noun_or_adjective(tok, tag):
            valid_words.append(tok.lower())
            word_indices.append(idx)

    unique_nodes = list(set(valid_words))
    if not unique_nodes:
        return []

    # Build co-occurrence graph (window N = 2, undirected)
    adjacency: Dict[str, Dict[str, float]] = {w: {} for w in unique_nodes}

    for i in range(len(tokens)):
        w1 = tokens[i].lower()
        if w1 not in adjacency:
            continue
        # Check window
        for j in range(i + 1, min(i + window_size + 1, len(tokens))):
            w2 = tokens[j].lower()
            if w2 in adjacency and w1 != w2:
                adjacency[w1][w2] = adjacency[w1].get(w2, 0.0) + 1.0
                adjacency[w2][w1] = adjacency[w2].get(w1, 0.0) + 1.0

    # PageRank
    ranks = pagerank_graph(adjacency, unique_nodes, d=0.85, max_iter=30, tol=0.0001)

    # Sort nodes by score
    sorted_nodes = sorted(ranks.items(), key=lambda x: x[1], reverse=True)
    num_keep = max(1, int(len(sorted_nodes) * top_fraction))
    top_words_set = {word for word, score in sorted_nodes[:num_keep]}

    # Step 5: Phrase Formation (collapse adjacent selected words)
    phrases = []
    current_phrase = []
    tokens_lower = [t.lower() for t in tokens]

    for t, t_low in zip(tokens, tokens_lower):
        if t_low in top_words_set:
            current_phrase.append(t)
        else:
            if current_phrase:
                phrases.append(" ".join(current_phrase))
                current_phrase = []
    if current_phrase:
        phrases.append(" ".join(current_phrase))

    # Calculate phrase scores (sum of constituent word scores)
    phrase_scores: Dict[str, float] = {}
    for p in phrases:
        p_clean = p.strip()
        if len(p_clean) < 3:
            continue
        p_words = p_clean.lower().split()
        score = sum(ranks.get(w, 0.0) for w in p_words)
        # normalize slightly by length to not artificially penalize single words
        norm_score = score / (1.0 + 0.2 * (len(p_words) - 1))
        if p_clean.lower() not in phrase_scores or norm_score > phrase_scores[p_clean.lower()]:
            phrase_scores[p_clean.lower()] = round(norm_score, 4)

    # Sort final keywords/phrases
    sorted_phrases = sorted(phrase_scores.items(), key=lambda x: x[1], reverse=True)

    result = []
    seen = set()
    for phrase, score in sorted_phrases:
        if phrase not in seen:
            seen.add(phrase)
            result.append({"keyword": phrase, "textrank_score": score})
            if len(result) >= max_keywords:
                break

    return result


def summarize_resume_textrank(
    text: str,
    num_sentences: int = 3
) -> str:
    """
    Extracts a 2-3 sentence executive summary of a candidate resume using Sentence TextRank.

    Edge weight between sentences Si and Sj:
      w_ij = |words(Si) ∩ words(Sj)| / (log(len(Si)) + log(len(Sj)))
    """
    sentences = _split_sentences(text)
    if not sentences:
        return ""
    if len(sentences) <= num_sentences:
        return " ".join(sentences)

    # Pre-tokenize sentences into lowercase word sets (without stopwords)
    sent_words = []
    for s in sentences:
        words = {w.lower() for w in _tokenize_words(s) if w.lower() not in DEFAULT_STOPWORDS and len(w) > 2}
        sent_words.append(words)

    # Build sentence graph
    n = len(sentences)
    adjacency: Dict[int, Dict[int, float]] = {i: {} for i in range(n)}

    for i in range(n):
        for j in range(i + 1, n):
            words_i = sent_words[i]
            words_j = sent_words[j]
            overlap = len(words_i & words_j)
            len_i = len(words_i)
            len_j = len(words_j)

            if overlap > 0 and len_i > 0 and len_j > 0:
                # Log-length normalization avoids bias toward overly long sentences
                denom = math.log(len_i + 1) + math.log(len_j + 1)
                weight = overlap / denom if denom > 0 else 0.0
                adjacency[i][j] = weight
                adjacency[j][i] = weight

    # PageRank
    ranks = pagerank_graph(adjacency, list(range(n)), d=0.85, max_iter=30)

    # Pick top sentences while preserving original order
    top_indices = sorted(ranks.items(), key=lambda x: x[1], reverse=True)[:num_sentences]
    ordered_indices = sorted([idx for idx, _ in top_indices])

    selected_sentences = [sentences[idx] for idx in ordered_indices]
    return " ".join(selected_sentences)
