<div align="center">

# MedAI Assistant

**AI-powered discharge follow-up dashboard for turning patient summaries into safer, structured care guidance.**

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Groq](https://img.shields.io/badge/Groq-Llama_3.1-F55036?style=flat-square)](https://groq.com)

</div>

---

## Overview

MedAI Assistant is a full-stack healthcare AI prototype with a Streamlit clinical dashboard and a FastAPI backend. It lets a user add patient discharge summaries, calculate a simple risk tier, generate structured follow-up instructions with Groq, and chat with an assistant that keeps short per-patient context.

This project is designed for portfolio demos, deployment practice, and AI workflow experimentation. It is not a certified clinical tool.

## Features

- Multi-patient dashboard built with Streamlit
- FastAPI REST backend deployable to Vercel
- SQLAlchemy persistence with SQLite locally or PostgreSQL in production
- Groq-powered instruction generation and patient Q&A
- Rule-based risk labels: `LOW`, `MEDIUM`, `HIGH`
- Backend health check for deployment debugging
- Safer prompt framing for medical assistant responses

## Architecture

```text
Streamlit Cloud
  app.py
  API_URL secret
       |
       | HTTPS
       v
Vercel FastAPI
  index.py -> backend.api:app
  GROQ_API_KEY secret
  DATABASE_URL secret
       |
       v
PostgreSQL provider
  Neon, Supabase, Railway, or another hosted database
```

## Project Structure

```text
.
├── app.py                    # Streamlit frontend
├── index.py                  # Vercel entrypoint for FastAPI
├── vercel.json               # Vercel Python routing
├── backend/
│   ├── api.py                # FastAPI app, CORS, router registration
│   ├── crud.py               # Database operations
│   ├── database.py           # SQLAlchemy engine/session
│   ├── models/patient.py     # Patient table model
│   └── routes/ai_routes.py   # API endpoints
├── core/
│   ├── ai_engine.py          # Groq client wrapper
│   ├── memory.py             # Chat memory formatting
│   ├── prompts.py            # AI prompt templates
│   └── risk.py               # Rule-based risk detection
└── requirements.txt
```

## API

### `GET /health`

Checks whether the backend is reachable.

```json
{
  "status": "ok"
}
```

### `POST /patients`

Creates a patient record and stores the discharge summary.

```json
{
  "name": "Muhammad Ali",
  "report": "Patient diagnosed with severe hypertension..."
}
```

### `GET /patients`

Returns all patient records, newest first.

### `POST /analyze`

Generates structured AI instructions from a discharge summary.

```json
{
  "report": "Patient discharged with chest pain precautions..."
}
```

### `POST /chat`

Asks a patient-specific question using the stored discharge summary and recent chat memory.

```json
{
  "patient_id": 1,
  "question": "What warning signs should I monitor?",
  "memory": ""
}
```

## Local Setup

```bash
git clone https://github.com/subata24/patient-followup-assistant.git
cd patient-followup-assistant
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Create `.env`:

```env
GROQ_API_KEY=your_groq_api_key
DATABASE_URL=sqlite:///./medai.db
API_URL=http://127.0.0.1:8000
```

Run the backend:

```bash
uvicorn backend.api:app --reload
```

Run the frontend in another terminal:

```bash
streamlit run app.py
```

Open:

- Streamlit app: `http://localhost:8501`
- FastAPI docs: `http://127.0.0.1:8000/docs`
- Health check: `http://127.0.0.1:8000/health`

## Deploy Backend To Vercel

1. Push this repository to GitHub.
2. Go to Vercel and import the GitHub repository.
3. Keep the framework preset as `Other`.
4. Add environment variables in Vercel:

```env
GROQ_API_KEY=your_groq_api_key
DATABASE_URL=your_postgres_connection_string
ALLOWED_ORIGINS=*
```

5. Use a hosted PostgreSQL database for `DATABASE_URL`. Good options are Neon, Supabase, or Railway. SQLite on Vercel is not persistent.
6. Deploy.
7. Open your Vercel backend URL and test:

```text
https://your-project.vercel.app/health
https://your-project.vercel.app/docs
```

## Connect Streamlit Cloud To Vercel API

1. Deploy the FastAPI backend on Vercel first.
2. Copy the Vercel production URL, for example:

```text
https://patient-followup-assistant-api.vercel.app
```

3. Open your Streamlit Cloud app dashboard.
4. Go to `Settings` -> `Secrets`.
5. Add:

```toml
API_URL = "https://patient-followup-assistant-api.vercel.app"
```

6. Save secrets and reboot the Streamlit app.
7. In the app, the top status should show `System Online`.
8. Add or load a demo patient. If the patient list updates, Streamlit is talking to Vercel successfully.

Important: `API_URL` must be the backend URL only, without `/patients`, `/health`, or any endpoint path.

## Production Notes

- Keep `.env` out of GitHub. Use Streamlit Secrets and Vercel Environment Variables instead.
- Use PostgreSQL for deployed storage. Vercel serverless functions do not provide durable SQLite storage.
- This project uses a simple keyword risk classifier. It is useful for demos, not clinical triage.
- The AI assistant is safety-framed, but all medical output must be reviewed by qualified clinicians.

## Disclaimer

MedAI Assistant is an educational proof of concept. It is not a medical device, does not diagnose, and must not replace emergency care or professional medical advice.

