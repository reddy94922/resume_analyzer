# utils/scoring.py
import re
from typing import List, Tuple
from collections import Counter

def keyword_score(resume_text: str, job_text: str) -> Tuple[float, dict]:
    """Compute a simple keyword overlap score. Returns (score_percent, details)."""
    def tokenize(s: str):
        return re.findall(r"\w+", s.lower())

    r_tokens = set(tokenize(resume_text))
    j_tokens = set(tokenize(job_text))
    # We focus on keywords longer than 3 chars to reduce noise
    j_keywords = {t for t in j_tokens if len(t) > 3}
    if not j_keywords:
        return 0.0, {"matched": [], "total": 0}
    matched = sorted(list(j_keywords & r_tokens))
    score = 100.0 * len(matched) / len(j_keywords)
    return score, {"matched": matched, "total_keywords": len(j_keywords)}

def semantic_score(vectorstore, resume_chunks: List[str], job_description: str, k: int = 5) -> Tuple[float, List[dict]]:
    """Do semantic similarity via vectorstore: for each job_description, search and compute simple normalized score.
    Returns (avg_score_percent, details)
    """
    # For simplicity: query vector store with job_description and compute how many hits above a threshold
    results = vectorstore.similarity_search_with_score(job_description, k=k)
    # results is list of tuples (Document, score) where score is distance — lower is better for FAISS
    # We'll convert to a 0-100 style score by mapping distance -> percent (this is heuristic)
    details = []
    import math
    max_score = 0.0
    for doc, score in results:
        # convert score (distance) to similarity estimate
        sim = 1.0 / (1.0 + math.exp(score))  # sigmoid-like mapping
        pct = sim * 100
        details.append({"text": doc.page_content[:200], "score": float(score), "pct": pct})
        if pct > max_score:
            max_score = pct
    # use max_score as the semantic match
    return max_score, details
