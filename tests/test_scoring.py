# tests/test_scoring.py
from utils.scoring import keyword_score

def test_keyword_score():
    resume = "Python, SQL, AWS, machine learning"
    jd = "We need experience with Python and AWS and Docker"
    score, details = keyword_score(resume, jd)
    assert score >= 0
    assert isinstance(details, dict)
