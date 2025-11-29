# main.py
from extractor.pdf_extractor import extract_text_from_pdf
from extractor.docx_extractor import extract_text_from_docx
from extractor.text_utils import clean_text, chunk_text
from embeddings.vectorstore_manager import build_or_load_vectorstore, semantic_search
from chains.analysis_chain import Analyzer
from utils.scoring import keyword_score, semantic_score
import os

def analyze_resume_file(resume_path: str, job_description: str, rebuild_index: bool = False, provider: str = None):
    if provider is None:
        provider = os.getenv("LLM_PROVIDER", "openai")
    
    ext = os.path.splitext(resume_path)[1].lower()
    if ext == ".pdf":
        raw = extract_text_from_pdf(resume_path)
    elif ext in (".docx", ".doc"):
        raw = extract_text_from_docx(resume_path)
    else:
        with open(resume_path, "r", encoding="utf-8") as f:
            raw = f.read()
    cleaned = clean_text(raw)
    chunks = chunk_text(cleaned)
    vs = build_or_load_vectorstore(chunks, rebuild=rebuild_index)

    analyzer = Analyzer(provider=provider)
    summary = analyzer.summarize(cleaned)
    skills_data = analyzer.extract_skills_and_experience(cleaned)
    strengths = analyzer.strengths_and_suggestions(cleaned)
    match_data = analyzer.match_with_job(summary, job_description)

    keyword_pct, keyword_details = keyword_score(cleaned, job_description)
    semantic_pct, semantic_details = semantic_score(vs, chunks, job_description)

    combined_pct = (keyword_pct * 0.4) + (semantic_pct * 0.6)

    result = {
        "summary": summary,
        "skills": skills_data,
        "strengths": strengths,
        "match_chain": match_data,
        "keyword_score": {"pct": keyword_pct, "details": keyword_details},
        "semantic_score": {"pct": semantic_pct, "details": semantic_details},
        "combined_match_pct": combined_pct,
    }
    return result

if __name__ == "__main__":
    # simple test runner
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--resume", required=True)
    parser.add_argument("--jd", required=True)
    parser.add_argument("--provider", default="openai", choices=["openai", "google"])
    args = parser.parse_args()
    res = analyze_resume_file(args.resume, args.jd, provider=args.provider)
    import json
    print(json.dumps(res, indent=2))
