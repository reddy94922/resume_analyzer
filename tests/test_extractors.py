# tests/test_extractors.py
from extractor.text_utils import clean_text, chunk_text

def test_clean_and_chunk():
    txt = """
    John Doe
    Page 1

    Experience:
    - Worked on X
    """
    cleaned = clean_text(txt)
    assert "Page" not in cleaned
    chunks = chunk_text(cleaned, max_tokens_estimate=10, overlap=2)
    assert len(chunks) >= 1
