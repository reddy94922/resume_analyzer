# extractor/pdf_extractor.py
import pdfplumber
from typing import List

def extract_text_from_pdf(path: str) -> str:
    """Extract text from PDF using pdfplumber. Returns concatenated text."""
    text_chunks: List[str] = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text() or ""
            text_chunks.append(page_text)
    return "\n".join(text_chunks).strip()
