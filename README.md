# 📄 Resume Parser — AI-Powered Candidate Analysis Tool

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green?style=flat&logo=fastapi)
![spaCy](https://img.shields.io/badge/NLP-spaCy-blue?style=flat)
![SQLite](https://img.shields.io/badge/Database-SQLite-orange?style=flat)
![Deployed](https://img.shields.io/badge/Deployed-Render.com-purple?style=flat)

> An end-to-end AI-powered Resume Parser that extracts structured information from PDF/DOCX resumes, scores job compatibility, and ranks multiple candidates — all from a clean, responsive web interface.

🔗 **Live Demo:** [https://resume-parser-ze3w.onrender.com](https://resume-parser-ze3w.onrender.com)

---

## ✨ Features

| Feature | Description |
|---|---|
| 📥 Resume Upload | Supports PDF and DOCX formats |
| 👤 Info Extraction | Extracts Name, Email, Phone using NLP |
| 🛠 Skills Detection | Matches against a curated skills list |
| 🎓 Education & Experience | Section-based structured parsing |
| 🎯 Job Match Score | % match between resume and job description |
| ✅ ATS Compatibility Score | Scores how ATS-friendly the resume is |
| 📊 Skills Breakdown Chart | Visual donut chart of skill categories |
| 🏆 Multi-Resume Ranking | Upload multiple resumes, rank by job fit |
| 🔍 Candidate Search | Filter ranked candidates by name or skill |
| 💾 History | All parsed resumes saved to SQLite database |
| 🌙 Dark/Light Mode | Toggle between themes |
| 📱 Mobile Responsive | Works on all screen sizes |

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | FastAPI, Python 3 |
| **NLP** | spaCy (en_core_web_sm) |
| **PDF Parsing** | pdfplumber |
| **DOCX Parsing** | python-docx |
| **Database** | SQLite + SQLAlchemy |
| **Frontend** | HTML, CSS, JavaScript |
| **Charts** | Chart.js |
| **Deployment** | Render.com |
| **Version Control** | GitHub |

---

## 🚀 Getting Started (Local Setup)

```bash
# 1. Clone the repo
git clone https://github.com/priya377/resume-parser.git
cd resume-parser

# 2. Install dependencies
pip install -r requirements.txt

# 3. Download spaCy model
python -m spacy download en_core_web_sm

# 4. Run the app
uvicorn main:app --reload
```

Open your browser at `http://127.0.0.1:8000`

---

## 📁 Project Structure

```text
resume-parser/
│
├── main.py                  # FastAPI backend + API endpoints
├── parse_resume_free.py     # NLP parsing + job matching logic
├── extract_text.py          # PDF/DOCX text extraction
├── database.py              # SQLite database models + CRUD
├── index.html               # Frontend UI
├── requirements.txt         # Python dependencies
└── uploads/                 # Uploaded resume files (auto-created)
```

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Serves the frontend UI |
| POST | `/upload-resume` | Parse a single resume |
| POST | `/upload-multiple-resumes` | Rank multiple resumes |
| GET | `/history` | Get all parsed resumes |
| DELETE | `/history/{id}` | Delete a resume record |

---

## 🎯 Use Cases

- **HR Teams** — Quickly screen and rank candidates
- **Job Portals** — Automate resume shortlisting
- **Recruiters** — Match candidates to job descriptions instantly
- **Job Seekers** — Check ATS score before applying

---

## 👩‍💻 Developer

**Priya** — Python & AI Developer  
🔗 [GitHub](https://github.com/priya377)  
🌐 [Live Project](https://resume-parser-ze3w.onrender.com)

---

⭐ If you found this useful, please give it a star!