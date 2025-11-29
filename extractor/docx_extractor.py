# extractor/docx_extractor.py
from docx import Document
from typing import List

def extract_text_from_docx(path: str) -> str:
    doc = Document(path)
    paragraphs: List[str] = [p.text for p in doc.paragraphs]
    return "\n".join(paragraphs).strip()
