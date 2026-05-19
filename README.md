<div align="center">

<img src="https://img.shields.io/badge/MedAI-Clinical%20Intelligence-0F6E56?style=for-the-badge&logoColor=white" alt="MedAI"/>

# MedAI — AI Clinical Discharge Intelligence Platform

**Turning hospital discharge summaries into actionable, AI-powered patient care instructions.**

[![Live Demo](https://img.shields.io/badge/🌐_Live_Demo-Streamlit_Cloud-FF4B4B?style=flat-square)](https://patient-followup-assistant-ed33mculwgncgfhejpvqfh.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?style=flat-square&logo=postgresql&logoColor=white)](https://postgresql.org)
[![Groq](https://img.shields.io/badge/Groq-LLaMA_3.1-F55036?style=flat-square)](https://groq.com)

</div>

---

## The problem

Hospitals discharge patients every day with complex instructions that are difficult to understand, lack structured follow-up guidance, and increase readmission risk. Post-discharge healthcare workflows remain inefficient and fragmented — placing the burden on patients who are least equipped to handle it.

## The solution

MedAI acts as an AI-powered clinical intelligence layer that transforms unstructured discharge summaries into structured, actionable care instructions for both healthcare professionals and patients — in seconds, in multiple languages.

---

## Features

### 🧠 AI clinical engine
Converts raw discharge summaries into structured medical guidance, extracting conditions, medications, diet plans, monitoring requirements, warning signs, and follow-up recommendations.

### ⚠️ Intelligent risk detection
Real-time patient risk scoring with three tiers — **Low**, **Medium**, and **High** — based on a rule-based clinical classifier. Automatically flags critical symptoms including chest pain, severe hypertension, dizziness, and cardiovascular warning signs.

### 🏥 Multi-patient SaaS dashboard
Add and manage multiple patients with persistent PostgreSQL-backed storage. Switch between patient records instantly on a scalable backend architecture.

### 💬 AI medical assistant
A ChatGPT-style clinical assistant with context-aware conversation memory for interactive patient guidance and AI-generated medical explanations.

### 📊 Admin analytics dashboard
Hospital-level monitoring with total patient overview, risk distribution visualization, and operational analytics.

### 🌍 Multilingual support
Patient instructions available in English and Urdu, with architecture ready for additional languages.

---

## Architecture
┌──────────────────────────────────────────────────────┐
│                  Streamlit Frontend                  │
│            Multi-patient SaaS Dashboard              │
└───────────────────────┬──────────────────────────────┘
│ HTTP
┌───────────────────────▼──────────────────────────────┐
│                   FastAPI Backend                    │
│          REST API  ·  Auth  ·  Background Tasks      │
└──────────┬────────────────────────────┬──────────────┘
│                            │
┌──────────▼──────────┐    ┌────────────▼─────────────┐
│    PostgreSQL DB     │    │        AI Layer           │
│  SQLAlchemy ORM      │    │  Groq LLaMA 3.1 API      │
│  Patient records     │    │  LangChain orchestration  │
│  Analysis history    │    │  Rule-based risk engine   │
└─────────────────────┘    └──────────────────────────┘

**Workflow:**
1. Doctor uploads a discharge summary via the dashboard
2. FastAPI backend processes the request asynchronously
3. AI engine generates structured medical instructions
4. Risk engine evaluates patient severity (Low / Medium / High)
5. PostgreSQL stores the patient record and analysis
6. Dashboard updates analytics in real time
7. AI assistant enables interactive clinical Q&A

---

## Tech stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Backend | FastAPI |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| AI model | Groq LLaMA 3.1 |
| Language | Python 3.11 |
| Risk engine | Rule-based classifier |
| Deployment | Streamlit Cloud |

---

## API reference

### `POST /analyze`
Submit a discharge summary for AI analysis.

**Request:**
```json
{
  "patient_id": "p_abc123",
  "patient_name": "Ali Hassan",
  "summary_text": "Patient discharged after cardiac episode...",
  "language": "english"
}
```

**Response:**
```json
{
  "status": "processing",
  "analysis_id": "a_xyz789"
}
```

### `GET /result/{analysis_id}`
Poll for analysis result.

```json
{
  "status": "complete",
  "risk_level": "High",
  "condition": "Acute myocardial infarction",
  "medications": ["Metoprolol 50mg", "Aspirin 75mg"],
  "care_plan": "...",
  "warning_signs": ["Chest pain", "Shortness of breath"]
}
```

### `GET /patients`
Fetch all patient records.

### `GET /patients/{patient_id}/history`
Fetch full analysis history for a patient.

---

## Getting started

### Prerequisites
- Python 3.11+
- PostgreSQL (or SQLite for local development)
- Groq API key — free at [console.groq.com](https://console.groq.com)

### Installation

```bash
git clone https://github.com/subata24/medai
cd medai
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Environment setup

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
DATABASE_URL=postgresql://user:password@localhost/medai
# For local dev without PostgreSQL:
# DATABASE_URL=sqlite:///./medai.db
```

### Run

```bash
# Backend
uvicorn main:app --reload
# Docs at: http://localhost:8000/docs

# Frontend
streamlit run app.py
```

---

## Project structure
medai/
├── main.py           # FastAPI app and all routes
├── ai.py             # Groq + LangChain AI logic
├── models.py         # SQLAlchemy database models
├── schemas.py        # Pydantic request/response schemas
├── database.py       # Database connection setup
├── app.py            # Streamlit frontend
├── .env              # Secrets (never commit this)
└── requirements.txt

---

## Engineering highlights

- Full-stack AI SaaS architecture with clean separation of concerns
- Async FastAPI backend with background task processing for non-blocking LLM calls
- PostgreSQL-backed persistent patient records with SQLAlchemy ORM
- Rule-based clinical risk classifier with keyword scoring
- Session-based AI conversation memory per patient
- Bilingual output (English + Urdu) with extensible language support
- Live deployment on Streamlit Cloud with public demo

---

## Roadmap

- [ ] JWT authentication and role-based access (doctor / admin)
- [ ] PDF discharge summary export
- [ ] Cloud database deployment (Railway / AWS RDS)
- [ ] Docker containerization
- [ ] Mobile patient portal
- [ ] Advanced analytics and readmission prediction
- [ ] Real-time monitoring and alerting
- [ ] FHIR-compatible patient data format

---

## Disclaimer

MedAI is a proof-of-concept AI healthcare platform built for educational and demonstration purposes. It is **not** a certified medical device and must not be used for medical diagnosis, emergency treatment, or as a replacement for clinical decision-making. Always consult licensed healthcare professionals.

---

## Author

**Subata Khan** — AI Engineer & LLM Systems Developer

[![LinkedIn](https://img.shields.io/badge/LinkedIn-subata--khan-0A66C2?style=flat-square&logo=linkedin)](https://www.linkedin.com/in/subata-khan-217712327/)
[![GitHub](https://img.shields.io/badge/GitHub-subata24-181717?style=flat-square&logo=github)](https://github.com/subata24)

