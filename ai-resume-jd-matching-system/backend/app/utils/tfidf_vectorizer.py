"""
TF-IDF Vectorizer for text similarity calculation
"""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import re


def preprocess_text(text: str) -> str:
    """Clean text for vectorization"""
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def calculate_cosine_similarity(text1: str, text2: str) -> float:
    """
    Calculate cosine similarity between two texts using TF-IDF
    
    Args:
        text1: First text (resume)
        text2: Second text (job description)
        
    Returns:
        Similarity score between 0 and 1
    """
    if not text1 or not text2:
        return 0.0

    cleaned1 = preprocess_text(text1)
    cleaned2 = preprocess_text(text2)

    try:
        vectorizer = TfidfVectorizer(
            max_features=5000,
            stop_words='english',
            ngram_range=(1, 2)  # unigrams and bigrams
        )

        tfidf_matrix = vectorizer.fit_transform([cleaned1, cleaned2])
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])

        return round(float(similarity[0][0]), 4)

    except Exception as e:
        print(f"Error calculating similarity: {e}")
        return 0.0


def calculate_keyword_density(resume_text: str, jd_text: str) -> float:
    """
    Calculate what percentage of JD keywords appear in resume
    
    Args:
        resume_text: Resume text
        jd_text: Job description text
        
    Returns:
        Keyword density score between 0 and 1
    """
    if not resume_text or not jd_text:
        return 0.0

    resume_lower = resume_text.lower()
    jd_lower = jd_text.lower()

    # Extract important words from JD (ignore stop words)
    stop_words = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to',
        'for', 'of', 'with', 'by', 'from', 'is', 'are', 'was', 'were',
        'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did',
        'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can',
        'this', 'that', 'these', 'those', 'we', 'you', 'he', 'she', 'it',
        'they', 'our', 'your', 'their', 'its', 'as', 'if', 'than', 'then'
    }

    jd_words = set(jd_lower.split()) - stop_words
    jd_words = {w for w in jd_words if len(w) > 3}  # ignore short words

    if not jd_words:
        return 0.0

    matched = sum(1 for word in jd_words if word in resume_lower)
    density = matched / len(jd_words)

    return round(min(density, 1.0), 4)
