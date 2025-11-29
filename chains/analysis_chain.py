# chains/analysis_chain.py
from typing import Dict, List
import os
import json

MODEL_NAME = "gpt-4o-mini"  # pick available model
GOOGLE_MODEL_NAME = "gemini-pro"  # Google Gemini model (or try gemini-pro for free tier)

# Raw prompt strings — PromptTemplate and LLMChain will be created at init-time
_SKILLS_PROMPT = {
    "input_variables": ["context"],
    "template": (
        "You are a helpful assistant that extracts skills and experience bullets from resume text.\n"
        "Context: {context}\n"
        "Return JSON with keys: skills (list), experience_bullets (list)."
    ),
}

_SUMMARY_PROMPT = {
    "input_variables": ["context"],
    "template": ("Summarize the candidate experience in 3-5 sentences.\nContext: {context}"),
}

_STRENGTHS_PROMPT = {
    "input_variables": ["context"],
    "template": (
        "Based on this resume context, list strengths and weaknesses (3 each) and provide short actionable suggestions.\nContext: {context}"
    ),
}

_MATCH_PROMPT = {
    "input_variables": ["resume_summary", "job_description"],
    "template": (
        "Compare the resume and the job description. Provide: \n"
        "1) a match percentage (0-100) \n"
        "2) brief explanation of matches & gaps\n"
        "Inputs:\nResume summary: {resume_summary}\nJob description: {job_description}\nReturn a JSON with keys: match_pct (number), explanation (string)."
    ),
}

# Google API helper (using REST API instead of SDK)
def _call_google_api(prompt_text: str, api_key: str = None) -> str:
    """Call Google Generative API (Gemini) via REST."""
    import requests
    if api_key is None:
        api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY or GOOGLE_API_KEY not set")
    
    # Use latest stable models (gemini-pro is deprecated)
    models_to_try = [
        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}",
        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent?key={api_key}",
        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}",
    ]
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt_text}
                ]
            }
        ]
    }
    
    last_error = None
    for url in models_to_try:
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=60)
            response.raise_for_status()
            result = response.json()
            if "candidates" in result and len(result["candidates"]) > 0:
                candidate = result["candidates"][0]
                if "content" in candidate and "parts" in candidate["content"]:
                    parts = candidate["content"]["parts"]
                    if len(parts) > 0 and "text" in parts[0]:
                        return parts[0]["text"]
            raise ValueError(f"Unexpected response structure: {result}")
        except requests.exceptions.RequestException as e:
            last_error = e
            continue
    
    raise ValueError(f"Google API call failed (all endpoints tried): {last_error}")


class Analyzer:
    def __init__(self, model_name: str = MODEL_NAME, temperature: float = 0.0, provider: str = "openai"):
        self.provider = provider
        self.model_name = model_name
        self.temperature = temperature

        if provider == "google":
            # Google provider — check API key is available
            api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
            if not api_key:
                raise ValueError("GEMINI_API_KEY or GOOGLE_API_KEY environment variable not set")
            self.google_api_key = api_key
            # No need to initialize LLMChain for Google; we'll call the API directly
            self.llm = None
            self.skills_chain = None
            self.summary_chain = None
            self.strengths_chain = None
            self.match_chain = None
        else:
            # OpenAI provider (default)
            from langchain_openai import ChatOpenAI
            # lazy/resilient imports to support different LangChain layouts
            PromptTemplate = None
            LLMChain = None
            try:
                from langchain_core.prompts import PromptTemplate as PT
                PromptTemplate = PT
            except Exception:
                try:
                    from langchain.prompts import PromptTemplate as PT
                    PromptTemplate = PT
                except Exception:
                    PromptTemplate = None

            # LLMChain may live in langchain_classic or other langchain packages depending on version
            try:
                from langchain_classic.chains import LLMChain as LC
                LLMChain = LC
            except Exception:
                try:
                    from langchain_core.chains import LLMChain as LC
                    LLMChain = LC
                except Exception:
                    try:
                        from langchain.chains import LLMChain as LC
                        LLMChain = LC
                    except Exception:
                        raise ImportError("Could not import LLMChain from langchain packages")

            self.llm = ChatOpenAI(model_name=model_name, temperature=temperature)

            # build PromptTemplate objects
            skills_prompt = PromptTemplate(input_variables=_SKILLS_PROMPT["input_variables"], template=_SKILLS_PROMPT["template"])
            summary_prompt = PromptTemplate(input_variables=_SUMMARY_PROMPT["input_variables"], template=_SUMMARY_PROMPT["template"])
            strengths_prompt = PromptTemplate(input_variables=_STRENGTHS_PROMPT["input_variables"], template=_STRENGTHS_PROMPT["template"])
            match_prompt = PromptTemplate(input_variables=_MATCH_PROMPT["input_variables"], template=_MATCH_PROMPT["template"])

            # create chains
            self.skills_chain = LLMChain(llm=self.llm, prompt=skills_prompt)
            self.summary_chain = LLMChain(llm=self.llm, prompt=summary_prompt)
            self.strengths_chain = LLMChain(llm=self.llm, prompt=strengths_prompt)
            self.match_chain = LLMChain(llm=self.llm, prompt=match_prompt)

    def extract_skills_and_experience(self, context: str) -> Dict:
        if self.provider == "google":
            prompt = _SKILLS_PROMPT["template"].format(context=context)
            out = _call_google_api(prompt, self.google_api_key)
        else:
            out = self.skills_chain.run(context=context)
        try:
            parsed = json.loads(out)
            return parsed
        except Exception:
            return {"raw": out}

    def summarize(self, context: str) -> str:
        if self.provider == "google":
            prompt = _SUMMARY_PROMPT["template"].format(context=context)
            return _call_google_api(prompt, self.google_api_key)
        else:
            return self.summary_chain.run(context=context)

    def strengths_and_suggestions(self, context: str) -> str:
        if self.provider == "google":
            prompt = _STRENGTHS_PROMPT["template"].format(context=context)
            return _call_google_api(prompt, self.google_api_key)
        else:
            return self.strengths_chain.run(context=context)

    def match_with_job(self, resume_summary: str, job_description: str) -> Dict:
        if self.provider == "google":
            prompt = _MATCH_PROMPT["template"].format(resume_summary=resume_summary, job_description=job_description)
            out = _call_google_api(prompt, self.google_api_key)
        else:
            out = self.match_chain.run(resume_summary=resume_summary, job_description=job_description)
        try:
            return json.loads(out)
        except Exception:
            return {"raw": out}
