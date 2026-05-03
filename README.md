# 🏥 AI Post-Discharge Patient Assistant

An AI-powered healthcare assistant that helps patients after hospital discharge by simplifying medical instructions, detecting risk symptoms, and providing safe follow-up guidance.

---

## 🚀 Features

- 🧠 AI-powered medical assistant (Groq LLM)
- 💬 Chat-based patient interaction
- ⚠️ Risk detection system (LOW / MEDIUM / HIGH)
- 🌍 English + Urdu medical support
- 🧾 Memory-based conversation system
- 📄 Patient report generation
- 🖥 Streamlit web interface

---

## 🏗 System Architecture
User → Streamlit UI → Risk Engine → Memory System → AI Model → Response

---

## ⚙️ Tech Stack

- Python
- Streamlit
- Groq API (LLaMA models)
- dotenv

---

## ▶️ Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py