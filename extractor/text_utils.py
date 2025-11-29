# extractor/text_utils.py
import re
from typing import List

def clean_text(text: str) -> str:
    """Basic cleaning: remove excessive whitespace, page headers/footers heuristics."""
    # Normalize whitespace
    t = re.sub(r"\r\n|\r", "\n", text)
    t = re.sub(r"\n{2,}", "\n\n", t)
    t = re.sub(r"[ \t]+", " ", t)
    # Remove repeating page numbers like '1 / 4' or 'Page 1'
    t = re.sub(r"Page\s+\d+", "", t, flags=re.I)
    t = re.sub(r"\b\d+\s*\/\s*\d+\b", "", t)
    return t.strip()

def chunk_text(text: str, max_tokens_estimate: int = 1000, overlap: int = 200) -> List[str]:
    """Simple word-based chunker. `max_tokens_estimate` is in words for simplicity."""
    words = text.split()
    if not words:
        return []

    # Ensure overlap is smaller than max chunk size to avoid infinite loops
    if overlap >= max_tokens_estimate:
        # set a sensible default overlap (half of chunk size)
        overlap = max(0, max_tokens_estimate // 2)

    stride = max_tokens_estimate - overlap
    if stride <= 0:
        stride = max(1, max_tokens_estimate // 2)

    chunks: List[str] = []
    for start in range(0, len(words), stride):
        end = min(start + max_tokens_estimate, len(words))
        chunks.append(" ".join(words[start:end]))
        if end >= len(words):
            break
    return chunks
