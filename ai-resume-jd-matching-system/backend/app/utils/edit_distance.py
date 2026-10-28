"""
edit_distance.py
─────────────────────────────────────────────────────────────────────────────
Custom implementation of Edit Distance (Levenshtein & Damerau-Levenshtein)
built completely from scratch without external dependencies.

Supports:
  1. Classic Levenshtein Distance (Insert, Delete, Substitute) with custom costs
  2. Damerau-Levenshtein Distance (adds Adjacent Character Transposition)
  3. Normalized Edit Similarity Ratio [0.0, 1.0]
  4. Dynamic Programming Matrix visualization / traceback
  5. Typo-tolerant Skill Matching for Resume & Job Description matching
     (e.g., handles "scikitlearn" -> "scikit-learn", "postgre" -> "postgresql")
─────────────────────────────────────────────────────────────────────────────
"""

from typing import List, Tuple, Dict, Optional, Any


def levenshtein_distance(
    s1: str,
    s2: str,
    insert_cost: int = 1,
    delete_cost: int = 1,
    substitute_cost: int = 1
) -> int:
    """
    Computes classic Levenshtein Distance between string s1 and string s2
    using a 2D dynamic programming table.

    Recurrence Relation:
      dp[i][j] = min(
          dp[i-1][j] + delete_cost,        # Deletion from s1
          dp[i][j-1] + insert_cost,        # Insertion into s1
          dp[i-1][j-1] + (0 if s1[i-1] == s2[j-1] else substitute_cost) # Substitution
      )

    Base cases:
      dp[i][0] = i * delete_cost
      dp[0][j] = j * insert_cost
    """
    m, n = len(s1), len(s2)

    # Fast path: identical strings
    if s1 == s2:
        return 0
    if m == 0:
        return n * insert_cost
    if n == 0:
        return m * delete_cost

    # Initialize (m+1) x (n+1) DP table
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = i * delete_cost
    for j in range(n + 1):
        dp[0][j] = j * insert_cost

    # Fill table
    for i in range(1, m + 1):
        c1 = s1[i - 1]
        for j in range(1, n + 1):
            c2 = s2[j - 1]
            cost_sub = 0 if c1 == c2 else substitute_cost
            dp[i][j] = min(
                dp[i - 1][j] + delete_cost,      # delete
                dp[i][j - 1] + insert_cost,      # insert
                dp[i - 1][j - 1] + cost_sub      # match/substitute
            )

    return dp[m][n]


def damerau_levenshtein_distance(
    s1: str,
    s2: str,
    insert_cost: int = 1,
    delete_cost: int = 1,
    substitute_cost: int = 1,
    transposition_cost: int = 1
) -> int:
    """
    Computes Damerau-Levenshtein Distance between string s1 and string s2.
    Extends Levenshtein by permitting transpositions of adjacent characters:
      e.g., 'teh' -> 'the' (distance 1 instead of 2).
    """
    m, n = len(s1), len(s2)

    if s1 == s2:
        return 0
    if m == 0:
        return n * insert_cost
    if n == 0:
        return m * delete_cost

    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = i * delete_cost
    for j in range(n + 1):
        dp[0][j] = j * insert_cost

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cost_sub = 0 if s1[i - 1] == s2[j - 1] else substitute_cost
            dp[i][j] = min(
                dp[i - 1][j] + delete_cost,      # deletion
                dp[i][j - 1] + insert_cost,      # insertion
                dp[i - 1][j - 1] + cost_sub      # substitution / match
            )

            # Check adjacent transposition
            if i > 1 and j > 1 and s1[i - 1] == s2[j - 2] and s1[i - 2] == s2[j - 1]:
                dp[i][j] = min(dp[i][j], dp[i - 2][j - 2] + transposition_cost)

    return dp[m][n]


def get_dp_matrix_and_alignment(
    s1: str,
    s2: str
) -> Dict[str, Any]:
    """
    Returns the complete DP matrix and the traceback alignment operations
    (Insert, Delete, Substitute, Match).
    Useful for educational demonstrations and explaining why two skills matched.
    """
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cost = 0 if s1[i - 1] == s2[j - 1] else 1
            dp[i][j] = min(
                dp[i - 1][j] + 1,       # delete
                dp[i][j - 1] + 1,       # insert
                dp[i - 1][j - 1] + cost # match or substitute
            )

    # Traceback optimal alignment path
    i, j = m, n
    operations = []
    while i > 0 or j > 0:
        if i > 0 and j > 0 and s1[i - 1] == s2[j - 1]:
            operations.append({"op": "match", "char_s1": s1[i - 1], "char_s2": s2[j - 1]})
            i -= 1
            j -= 1
        elif i > 0 and j > 0 and dp[i][j] == dp[i - 1][j - 1] + 1:
            operations.append({"op": "substitute", "char_s1": s1[i - 1], "char_s2": s2[j - 1]})
            i -= 1
            j -= 1
        elif i > 0 and dp[i][j] == dp[i - 1][j] + 1:
            operations.append({"op": "delete", "char_s1": s1[i - 1], "char_s2": None})
            i -= 1
        else:
            operations.append({"op": "insert", "char_s1": None, "char_s2": s2[j - 1]})
            j -= 1

    operations.reverse()

    return {
        "s1": s1,
        "s2": s2,
        "distance": dp[m][n],
        "dp_matrix": dp,
        "operations": operations
    }


def edit_similarity(s1: str, s2: str, algorithm: str = "damerau") -> float:
    """
    Calculates normalized Edit Similarity Ratio in range [0.0, 1.0].
    
    Formula:
        similarity = 1.0 - (distance / max(len(s1), len(s2)))
    """
    s1_clean = s1.lower().strip()
    s2_clean = s2.lower().strip()

    if s1_clean == s2_clean:
        return 1.0

    max_len = max(len(s1_clean), len(s2_clean))
    if max_len == 0:
        return 1.0

    if algorithm == "damerau":
        dist = damerau_levenshtein_distance(s1_clean, s2_clean)
    else:
        dist = levenshtein_distance(s1_clean, s2_clean)

    sim = 1.0 - (dist / max_len)
    return round(max(0.0, min(1.0, sim)), 4)


def find_closest_skill(
    candidate: str,
    target_skills: List[str],
    max_distance: int = 2,
    min_similarity: float = 0.80
) -> Optional[Dict[str, Any]]:
    """
    Finds the closest matching skill in target_skills using Edit Distance.
    Matches if distance <= max_distance OR similarity >= min_similarity.
    """
    cand_lower = candidate.lower().strip()
    if not cand_lower:
        return None

    best_match = None
    best_dist = float("inf")
    best_sim = 0.0

    for target in target_skills:
        t_lower = target.lower().strip()
        if cand_lower == t_lower:
            return {
                "matched_skill": target,
                "query": candidate,
                "distance": 0,
                "similarity": 1.0,
                "is_exact": True
            }

        dist = damerau_levenshtein_distance(cand_lower, t_lower)
        max_l = max(len(cand_lower), len(t_lower))
        sim = 1.0 - (dist / max_l) if max_l > 0 else 0.0

        if dist < best_dist or (dist == best_dist and sim > best_sim):
            best_dist = dist
            best_sim = sim
            best_match = target

    if best_match and (best_dist <= max_distance or best_sim >= min_similarity):
        return {
            "matched_skill": best_match,
            "query": candidate,
            "distance": best_dist,
            "similarity": round(best_sim, 4),
            "is_exact": best_dist == 0
        }

    return None


def fuzzy_match_skills(
    resume_skills: List[str],
    jd_skills: List[str],
    max_distance: int = 2,
    min_similarity: float = 0.80
) -> Dict[str, Any]:
    """
    Compares resume skills against required JD skills with typo tolerance.
    
    Identifies:
      - Exact matches (distance 0)
      - Fuzzy matches (distance 1 or 2, e.g. "scikit learn" -> "scikit-learn")
      - Missing skills (unmatched JD skills)
      - Extra skills (candidate skills beyond JD requirements)
    """
    resume_set = {s.strip() for s in resume_skills if s and s.strip()}
    jd_set = {s.strip() for s in jd_skills if s and s.strip()}

    exact_matches = []
    fuzzy_matches = []
    matched_jd_skills = set()
    used_resume_skills = set()

    # Pass 1: Exact matches (case-insensitive)
    for r_skill in resume_set:
        r_lower = r_skill.lower()
        for jd_skill in jd_set:
            if r_lower == jd_skill.lower():
                exact_matches.append(jd_skill)
                matched_jd_skills.add(jd_skill)
                used_resume_skills.add(r_skill)
                break

    # Pass 2: Edit Distance fuzzy matching for remaining unmatched skills
    remaining_jd = jd_set - matched_jd_skills
    remaining_resume = resume_set - used_resume_skills

    for r_skill in remaining_resume:
        match_info = find_closest_skill(
            r_skill,
            list(remaining_jd),
            max_distance=max_distance,
            min_similarity=min_similarity
        )
        if match_info:
            matched_jd = match_info["matched_skill"]
            fuzzy_matches.append({
                "resume_skill": r_skill,
                "jd_skill": matched_jd,
                "edit_distance": match_info["distance"],
                "edit_similarity": match_info["similarity"]
            })
            matched_jd_skills.add(matched_jd)
            remaining_jd.discard(matched_jd)

    missing_skills = list(jd_set - matched_jd_skills)
    total_matched = len(exact_matches) + len(fuzzy_matches)
    match_percentage = round((total_matched / len(jd_set)) * 100, 2) if jd_set else 0.0

    return {
        "exact_matches": exact_matches,
        "fuzzy_matches": fuzzy_matches,
        "total_exact": len(exact_matches),
        "total_fuzzy": len(fuzzy_matches),
        "all_matched_skills": list(matched_jd_skills),
        "missing_skills": missing_skills,
        "skill_match_percentage": match_percentage,
        "algorithm": "custom_damerau_levenshtein_dp"
    }
