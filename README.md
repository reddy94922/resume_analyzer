# 📄 Resume Analyzer

A powerful web application that analyzes resumes and matches them against job descriptions using AI. Get instant feedback on how well your resume aligns with the job requirements.

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.51-red)
![LangChain](https://img.shields.io/badge/LangChain-1.1-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 🎯 Features

- **📤 Resume Upload** - Support for PDF, DOCX, and TXT formats
- **🤖 AI Analysis** - Uses Google Gemini 2.5 to analyze resume content
- **📊 Match Scoring** - Get a comprehensive match percentage with the job description
  - Overall match score (0-100%)
  - Keyword match percentage
  - Semantic similarity score
- **💡 Actionable Insights**
  - Key strengths highlighted
  - Areas for improvement
  - Specific tips to boost your score
- **💼 Skills Extraction** - Automatically identifies skills and experience
- **📥 Export Results** - Download analysis as JSON or text report
- **🎨 Beautiful UI** - Clean, intuitive interface with color-coded feedback

---

## 🚀 Quick Start

### Prerequisites
- Python 3.13+
- Gemini API key (free at [Google AI Studio](https://aistudio.google.com))

### Installation

1. **Clone/Download the project**
   ```bash
   cd resume_analyzer
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment**
   - **Windows:**
     ```bash
     .\venv\Scripts\activate
     ```
   - **macOS/Linux:**
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables**
   
   Create a `.env` file in the project root:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   OPENAI_API_KEY=your_openai_api_key_here (optional)
   LLM_PROVIDER=google
   ```

6. **Run the app**
   ```bash
   streamlit run streamlit_app.py
   ```

7. **Open in browser**
   - Local: `http://localhost:8502`
   - Network: `http://<your-ip>:8502`

---

## 📖 How to Use

### Step 1: Upload Resume
Click the file uploader and select your resume file:
- **PDF** (.pdf)
- **DOCX** (.docx)
- **TXT** (.txt)

### Step 2: Add Job Description
Either:
- Paste the job description in the text area, OR
- Upload a TXT file with the job description

### Step 3: Click Analyze
Click the "🚀 Analyze Resume" button and wait for results.

### Step 4: Review Results

The analysis shows:

1. **🎯 Match Scores**
   - Overall match percentage
   - Keyword match (exact skills mentioned)
   - Semantic match (AI-detected relevance)

2. **📝 Resume Summary**
   - Key highlights of your resume

3. **💼 Extracted Skills & Experience**
   - Identified technical skills
   - Experience highlights

4. **💡 Key Insights**
   - ✅ Your Strengths (top 5)
   - ⚠️ Areas to Improve (top 5)
   - 🎯 How to Improve Your Score (actionable tips)

5. **📊 Score Breakdown**
   - Detailed keyword matching
   - Semantic similarity details

### Step 5: Download Results
Export your analysis:
- **Full Analysis (JSON)** - Complete raw data
- **Text Report** - Formatted report for sharing

---

## 🛠️ Architecture

### Project Structure
```
resume_analyzer/
├── main.py                      # Entry point for analysis
├── streamlit_app.py            # Web UI
├── requirements.txt            # Dependencies
├── .env                        # API keys (DO NOT COMMIT)
│
├── chains/
│   └── analysis_chain.py       # LLM orchestration (Gemini/OpenAI)
│
├── embeddings/
│   └── vectorstore_manager.py  # Vector store (FAISS) + embeddings (TF-IDF)
│
├── extractor/
│   ├── pdf_extractor.py        # PDF text extraction
│   ├── docx_extractor.py       # DOCX text extraction
│   └── text_utils.py           # Text cleaning & chunking
│
├── utils/
│   └── scoring.py              # Keyword & semantic scoring
│
├── tests/
│   ├── test_extractors.py      # Extract tests
│   └── test_scoring.py         # Scoring tests
│
└── .streamlit/
    └── config.toml             # Streamlit configuration
```

### Technology Stack
| Component | Technology | Purpose |
|-----------|-----------|---------|
| **LLM** | Google Gemini 2.5 | Resume analysis & insights |
| **Orchestration** | LangChain 1.1 | LLM chain management |
| **Embeddings** | TF-IDF (scikit-learn) | Free semantic search (no quota) |
| **Vector Store** | FAISS | Fast similarity search |
| **Web UI** | Streamlit 1.51 | Beautiful interface |
| **File Extraction** | pdfplumber, python-docx | PDF/DOCX parsing |

---

## 🔑 Getting API Keys

### Google Gemini (Recommended - Free Tier)
1. Go to [Google AI Studio](https://aistudio.google.com)
2. Click "Get API Key"
3. Create a new project or use existing one
4. Copy the API key
5. Add to `.env`: `GEMINI_API_KEY=your_key`

### OpenAI (Optional - Paid)
1. Go to [OpenAI API Keys](https://platform.openai.com/api-keys)
2. Create a new API key
3. Ensure billing is enabled
4. Add to `.env`: `OPENAI_API_KEY=your_key`
5. Change LLM provider: `LLM_PROVIDER=openai`

---

## 📊 How Scoring Works

### Keyword Match (40%)
- Extracts keywords from job description
- Counts exact matches in resume
- Formula: `(matched_keywords / total_keywords) * 100`

### Semantic Match (40%)
- Uses FAISS vector store for similarity search
- Compares semantic meaning beyond keywords
- Formula: `AI similarity score * 100`

### Combined Score (20%)
- Weighted average of both scoring methods
- Prioritizes keyword match slightly

---

## 🧪 Testing

Run tests to verify installation:
```bash
pytest tests/ -v
```

### Test Files
- `test_extractors.py` - Text extraction validation
- `test_scoring.py` - Scoring algorithm verification

---

## 📝 Environment Variables

### Required
```env
GEMINI_API_KEY=your_gemini_key_here
```

### Optional
```env
OPENAI_API_KEY=your_openai_key_here
LLM_PROVIDER=google  # or 'openai'
```

### ⚠️ Security
- **Never commit `.env` to git**
- Add to `.gitignore` (already done)
- Use `.env.example` for templates

---

## 🚨 Troubleshooting

### "Gemini API key not found"
- Ensure `.env` file exists in project root
- Check `GEMINI_API_KEY` is set correctly
- Restart Streamlit app

### "404 Not Found" error
- Verify API key is valid (check Google AI Studio)
- Ensure "Google AI for Developers API" is enabled
- Try with `gemini-2.5-flash` model

### "PDF extraction failed"
- Ensure file is valid PDF
- Try converting to TXT if issues persist
- Check `pdfplumber` is installed

### "ModuleNotFoundError"
- Activate virtual environment
- Run `pip install -r requirements.txt`
- Restart terminal

### Slow analysis
- First run builds embeddings (slower)
- Subsequent runs use cached embeddings
- Check internet connection for API calls

---

## 📋 Requirements

```
python-dotenv>=1.0.0
streamlit>=1.51.0
langchain>=1.1.0
langchain-google-genai>=0.1.0
langchain-community>=0.4.1
langchain-core>=1.1.0
faiss-cpu>=1.13.0
pdfplumber>=0.10.0
python-docx>=0.8.11
scikit-learn>=1.3.0
requests>=2.31.0
pytest>=7.4.0
```

---

## 🎯 Tips for Better Scores

1. **Use Keywords** - Include job description keywords in your resume
2. **Be Specific** - Use quantifiable achievements ("Improved by 25%")
3. **Match Format** - Use same terminology as job description
4. **Include Certifications** - Add relevant training and certifications
5. **Highlight Results** - Focus on impact and outcomes
6. **Customize for Role** - Tailor resume for each job application

---

## 🔄 Supported File Formats

| Format | Extension | Supported |
|--------|-----------|-----------|
| PDF | `.pdf` | ✅ Yes |
| Word | `.docx` | ✅ Yes |
| Text | `.txt` | ✅ Yes |
| Rich Text | `.rtf` | ⚠️ Not yet |
| Image PDF | `.pdf` | ⚠️ Limited |

---

## 📄 Output Examples

### Match Score Interpretation
- **80-100%** - Excellent match ✅
- **60-79%** - Good match 👍
- **40-59%** - Moderate match ⚠️
- **Below 40%** - Needs improvement 📈

### Downloaded JSON Includes
```json
{
  "summary": "...",
  "skills": {...},
  "strengths": "...",
  "match_chain": {...},
  "keyword_score": {"score": 75, "matched": [...]},
  "semantic_score": {"pct": 82},
  "combined_match_pct": 78.5
}
```

---

## 🚀 Deployment

### Streamlit Cloud (Free)
1. Push project to GitHub
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Deploy directly from repo
4. Add API keys in app secrets

### Docker (Self-Hosted)
```bash
docker build -t resume-analyzer .
docker run -p 8502:8502 -e GEMINI_API_KEY=your_key resume-analyzer
```

### Manual Server
```bash
streamlit run streamlit_app.py --server.port 80 --server.address 0.0.0.0
```

---

## 📞 Support & Issues

- Check existing issues on GitHub
- Verify API keys are valid
- Test with sample files provided
- Check terminal output for error messages
- Ensure all dependencies are installed

---

## 📜 License

MIT License - Feel free to use and modify

---

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io)
- LLM orchestration via [LangChain](https://langchain.com)
- AI powered by [Google Gemini](https://gemini.google.com)
- Vector search by [FAISS](https://github.com/facebookresearch/faiss)

---

## 📈 Future Enhancements

- [ ] Multi-language support
- [ ] Resume comparison tool
- [ ] Salary range prediction
- [ ] Industry-specific analysis
- [ ] LinkedIn profile integration
- [ ] Batch resume analysis
- [ ] Mobile app version

---

**Happy resume analyzing! 🚀**
