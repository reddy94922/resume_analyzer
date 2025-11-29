# streamlit_app.py
import streamlit as st
from main import analyze_resume_file
import tempfile
import os
import json
from dotenv import load_dotenv
import re
load_dotenv()

st.set_page_config(page_title="Resume Analyzer", layout="wide")

# Custom CSS for better styling
st.markdown("""
<style>
    .score-high { color: #28a745; font-weight: bold; }
    .score-medium { color: #ffc107; font-weight: bold; }
    .score-low { color: #dc3545; font-weight: bold; }
    .tip-box {
        background-color: #e7f3ff;
        padding: 15px;
        border-radius: 5px;
        border-left: 4px solid #2196F3;
        margin: 10px 0;
    }
    .weakness-box {
        background-color: #ffe7e7;
        padding: 15px;
        border-radius: 5px;
        border-left: 4px solid #dc3545;
        margin: 10px 0;
    }
    .strength-box {
        background-color: #e7ffe7;
        padding: 15px;
        border-radius: 5px;
        border-left: 4px solid #28a745;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# API key handling
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY and "GEMINI_API_KEY" not in st.secrets:
    st.warning("⚠️ Gemini API key not found. Set GEMINI_API_KEY as an environment variable or use .streamlit/secrets.toml.")

st.title("📄 Resume Analyzer")
st.markdown("Get instant feedback on how well your resume matches the job description")

with st.sidebar:
    st.header("⚙️ Settings")
    rebuild = st.checkbox("Rebuild embeddings/index", value=False)
    llm_provider = st.selectbox("LLM Provider", ["Google Gemini", "OpenAI"], index=0)

uploaded_file = st.file_uploader("📤 Upload resume (PDF/DOCX/TXT)", type=["pdf","docx","txt"])
job_desc = st.text_area("📋 Paste job description", height=150)
job_file = st.file_uploader("📤 Or upload job description (TXT)", type=["txt"]) 

if job_file and not job_desc:
    job_desc = job_file.getvalue().decode("utf-8")

if st.button("🚀 Analyze Resume", use_container_width=True):
    if not uploaded_file:
        st.error("❌ Please upload a resume file.")
    elif not job_desc:
        st.error("❌ Please provide a job description.")
    else:
        with st.spinner("⏳ Processing your resume and analyzing match..."):
            # Save uploaded file to a temp path
            suffix = os.path.splitext(uploaded_file.name)[1]
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                tmp.write(uploaded_file.getbuffer())
                tmp_path = tmp.name
            try:
                res = analyze_resume_file(tmp_path, job_desc, rebuild_index=rebuild)
                st.success("✅ Analysis complete!")
                
                # Match Score - Prominent Display
                score = res.get('combined_match_pct', 0)
                col1, col2, col3 = st.columns(3)
                with col1:
                    if score >= 80:
                        st.metric("🎯 Match Score", f"{score:.0f}%", delta="Excellent", delta_color="inverse")
                    elif score >= 60:
                        st.metric("🎯 Match Score", f"{score:.0f}%", delta="Good", delta_color="off")
                    else:
                        st.metric("🎯 Match Score", f"{score:.0f}%", delta="Needs Work")
                
                with col2:
                    keyword_score = res.get("keyword_score", {}).get("score", 0)
                    st.metric("🔑 Keywords Match", f"{keyword_score:.0f}%")
                
                with col3:
                    semantic_score = res.get("semantic_score", {}).get("pct", 0)
                    st.metric("🧠 Semantic Match", f"{semantic_score:.0f}%")
                
                # Resume Summary
                st.subheader("📝 Resume Summary")
                with st.expander("View Summary", expanded=True):
                    st.write(res.get("summary", "No summary available"))
                
                # Skills Extraction
                st.subheader("💼 Extracted Skills & Experience")
                skills_data = res.get("skills", {})
                if isinstance(skills_data, dict) and "raw" not in skills_data:
                    cols = st.columns(2)
                    with cols[0]:
                        if "skills" in skills_data:
                            st.write("**Skills:**")
                            for skill in skills_data.get("skills", [])[:10]:
                                st.write(f"• {skill}")
                    with cols[1]:
                        if "experience" in skills_data:
                            st.write("**Experience:**")
                            exp = skills_data.get("experience", "")
                            if isinstance(exp, list):
                                for item in exp[:5]:
                                    st.write(f"• {item}")
                            else:
                                st.write(f"• {exp[:200]}...")
                else:
                    with st.expander("View Extracted Data"):
                        st.json(skills_data)
                
                # Strengths & Weaknesses - Simplified
                st.subheader("💡 Key Insights")
                strengths_text = res.get("strengths", "")
                
                # Parse and highlight key points
                if strengths_text:
                    lines = strengths_text.split('\n')
                    
                    strengths = []
                    weaknesses = []
                    tips = []
                    
                    current_section = None
                    for line in lines:
                        line = line.strip()
                        if not line:
                            continue
                        
                        if "strength" in line.lower():
                            current_section = "strengths"
                        elif "weakness" in line.lower() or "suggestion" in line.lower() or "improvement" in line.lower():
                            current_section = "weaknesses"
                        elif "tip" in line.lower() or "recommendation" in line.lower():
                            current_section = "tips"
                        elif current_section and line.startswith(('•', '-', '*', '1', '2', '3', '4', '5')):
                            # Clean the line
                            clean_line = re.sub(r'^[•\-*\d.)\s]+', '', line).strip()
                            if clean_line:
                                if current_section == "strengths":
                                    strengths.append(clean_line)
                                elif current_section == "weaknesses":
                                    weaknesses.append(clean_line)
                                elif current_section == "tips":
                                    tips.append(clean_line)
                    
                    # Display Strengths
                    if strengths:
                        st.markdown("### ✅ Your Strengths")
                        for strength in strengths[:5]:  # Show top 5
                            st.markdown(f'<div class="strength-box"><strong>✓</strong> {strength}</div>', unsafe_allow_html=True)
                    
                    # Display Weaknesses/Areas to Improve
                    if weaknesses:
                        st.markdown("### ⚠️ Areas to Improve")
                        for i, weakness in enumerate(weaknesses[:5], 1):  # Show top 5
                            st.markdown(f'<div class="weakness-box"><strong>{i}.</strong> {weakness}</div>', unsafe_allow_html=True)
                    
                    # Display Tips to Improve Score
                    if not tips:
                        # Generate actionable tips from analysis
                        tips = [
                            f"Add specific projects that use the required technologies",
                            f"Highlight {res.get('keyword_score', {}).get('total_keywords', 0)} key job requirements in your resume",
                            f"Use action verbs and quantifiable achievements (e.g., 'Improved performance by X%')",
                            f"Include relevant certifications or training",
                            f"Tailor your summary to emphasize job-relevant skills"
                        ]
                    
                    st.markdown("### 🎯 How to Improve Your Score")
                    for i, tip in enumerate(tips[:5], 1):
                        st.markdown(f'<div class="tip-box"><strong>Tip {i}:</strong> {tip}</div>', unsafe_allow_html=True)
                
                # Score Breakdown
                st.subheader("📊 Detailed Score Breakdown")
                score_col1, score_col2 = st.columns(2)
                
                with score_col1:
                    st.write("**Keyword Match Details:**")
                    keyword_data = res.get("keyword_score", {})
                    st.write(f"• Matched: {keyword_data.get('matched', [])[:10]}")
                    st.write(f"• Total Keywords in Job: {keyword_data.get('total_keywords', 0)}")
                
                with score_col2:
                    st.write("**Semantic Match Details:**")
                    semantic_data = res.get("semantic_score", {})
                    st.write(f"• Overall Match: {semantic_data.get('pct', 0):.1f}%")
                
                # Download Section
                st.divider()
                col1, col2 = st.columns(2)
                with col1:
                    json_str = json.dumps(res, indent=2)
                    st.download_button(
                        label="📥 Download Full Analysis (JSON)",
                        data=json_str,
                        file_name="resume_analysis.json",
                        use_container_width=True
                    )
                
                with col2:
                    # Generate a text report
                    report = f"""RESUME ANALYSIS REPORT
=======================

Match Score: {score:.1f}%
Keyword Match: {res.get('keyword_score', {}).get('score', 0):.0f}%
Semantic Match: {res.get('semantic_score', {}).get('pct', 0):.0f}%

SUMMARY:
{res.get('summary', '')}

KEY AREAS TO IMPROVE:
{strengths_text}
"""
                    st.download_button(
                        label="📥 Download Text Report",
                        data=report,
                        file_name="resume_report.txt",
                        use_container_width=True
                    )
            finally:
                os.unlink(tmp_path)
