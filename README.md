<div align="center">

# MedAI Assistant

**AI-powered discharge follow-up dashboard that turns patient summaries into structured care guidance, risk signals, and patient-specific Q&A.**

[![Open App](https://img.shields.io/badge/Open_Live_App-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://medai-assistant-w6hqdj4lg7gawdpgjrvde2.streamlit.app/)
[![API](https://img.shields.io/badge/API-Vercel-black?style=for-the-badge&logo=vercel&logoColor=white)](https://med-ai-assistant-pi.vercel.app/health)

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=flat-square&logo=docker&logoColor=white)](https://www.docker.com/)
[![Groq](https://img.shields.io/badge/Groq-Llama_3.1-F55036?style=flat-square)](https://groq.com)

</div>

---

## Live Demo

- App: https://medai-assistant-w6hqdj4lg7gawdpgjrvde2.streamlit.app/
- API health check: https://med-ai-assistant-pi.vercel.app/health
- API docs: https://med-ai-assistant-pi.vercel.app/docs

## Overview

MedAI Assistant is a full-stack healthcare AI prototype with a Streamlit clinical dashboard and a FastAPI backend. Users can add discharge summaries, store patient records, calculate a simple risk tier, generate structured follow-up instructions with Groq, and ask patient-specific questions through an AI assistant with short-term conversation memory.

This project is built for portfolio demos, deployment practice, and AI workflow experimentation. It is not a certified medical product.

## Features

- Multi-patient dashboard built with Streamlit
- FastAPI REST backend deployed on Vercel
- Dockerized Streamlit app for reproducible local/container runs
- SQLAlchemy persistence with local SQLite or hosted PostgreSQL
- Groq-powered discharge instruction generation
- Patient-specific AI chat with recent conversation memory
- Rule-based risk labels: `LOW`, `MEDIUM`, `HIGH`
- Backend health endpoint for deployment debugging
- Safer medical prompt framing and basic prompt-injection resistance

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
Hosted PostgreSQL
  Neon, Supabase, Railway, or another provider
```

## Project Structure

```text
.
|-- app.py                    # Streamlit frontend
|-- index.py                  # Vercel entrypoint for FastAPI
|-- vercel.json               # Vercel Python routing
|-- Dockerfile                # Container image for the Streamlit app
|-- .dockerignore             # Keeps secrets and local files out of Docker builds
|-- backend/
|   |-- api.py                # FastAPI app and CORS
|   |-- crud.py               # Database operations
|   |-- database.py           # SQLAlchemy engine/session
|   |-- models/patient.py     # Patient table model
|   `-- routes/ai_routes.py   # API endpoints
|-- core/
|   |-- ai_engine.py          # Groq client wrapper
|   |-- memory.py             # Chat memory formatting
|   |-- prompts.py            # AI prompt templates
|   `-- risk.py               # Rule-based risk detection
`-- requirements.txt
```

## API Endpoints

### `GET /health`

Returns backend status.

```json
{
  "status": "ok"
}
```

### `POST /patients`

Creates a patient record.

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

Answers a patient-specific question using the stored summary and recent chat memory.

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

## Docker

The repository includes a Dockerfile for running the Streamlit frontend in a container.

Build the image:

```bash
docker build -t medai-assistant .
```

Run the container:

```bash
docker run --env-file .env -p 8501:8501 medai-assistant
```

If the backend is running on your host machine, set `API_URL` in `.env` to a reachable address for Docker. On Docker Desktop for Windows, use:

```env
API_URL=http://host.docker.internal:8000
```

For production, pass deployed service URLs through environment variables instead of copying secrets into the image.

## Deployment

### Vercel Backend

Add these environment variables in Vercel:

```env
GROQ_API_KEY=your_groq_api_key
DATABASE_URL=your_hosted_postgres_connection_string
ALLOWED_ORIGINS=*
```

Use hosted PostgreSQL for production. Do not use `localhost` in Vercel because it points to the serverless environment, not your laptop.

### Streamlit Frontend

Add this in Streamlit Cloud secrets:

```toml
API_URL = "https://med-ai-assistant-pi.vercel.app"
```

The value must be the API base URL only. Do not append `/health`, `/patients`, or `/docs`.

## Production Notes

- Keep `.env` out of GitHub.
- Store secrets in Streamlit Cloud and Vercel environment variables.
- Rotate any API key that has been exposed publicly.
- Use PostgreSQL for deployed storage because Vercel does not provide durable SQLite storage.
- The risk classifier is a simple rule-based demo, not clinical triage.

## Disclaimer

MedAI Assistant is an educational proof of concept. It is not a medical device, does not diagnose, and must not replace emergency care or professional medical advice.
