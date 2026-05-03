# 🏥 AI Post-Discharge Care Assistant

> An AI-powered healthcare support system that helps patients understand post-discharge instructions, detect risk symptoms, and receive guidance in simple English and Urdu.

---

## 🚀 Live Demo
👉 https://patient-followup-assistant-wm5neln6tzbvck3ysdk4p9.streamlit.app/

---

## 📌 Problem Statement

After hospital discharge, many patients:

- Misunderstand medical instructions  
- Forget medication schedules  
- Ignore early warning symptoms  
- Face language barriers (English ↔ Urdu)  
- Lack continuous medical guidance  

This leads to:

- ❌ Preventable complications  
- ❌ Hospital readmissions  
- ❌ Poor recovery outcomes  

---

## 💡 Solution

This system acts as a **24/7 AI medical assistant** that:

- Converts discharge summaries into structured instructions  
- Detects patient risk levels in real-time  
- Provides multilingual (English + Urdu) explanations  
- Maintains conversation memory for better guidance  
- Gives safe, simple, and actionable health advice  

---

## ⚙️ Key Features

### 🧠 AI Instruction Engine
Converts raw medical text into structured instructions:
- Condition  
- Medication  
- Diet  
- Monitoring  
- Warning  

---

### ⚠️ Risk Detection System
Classifies patient queries into:

- 🟢 Low Risk  
- 🟡 Medium Risk  
- 🔴 High Risk (e.g., chest pain, dizziness, emergency symptoms)

Automatically triggers safety warnings when needed.

---

### 🌍 Multilingual Support
- English → Simple patient-friendly instructions  
- Urdu → Accurate medical translation  

---

### 🧠 Conversation Memory
- Stores recent chat history  
- Improves contextual responses  
- Prevents repetitive answers  

---

### 🤖 LLM Integration
- Powered by Groq API (LLaMA models)  
- Fast inference for real-time responses  
- Optimized for instruction generation  

---

## 🏗️ System Architecture
User
↓
Streamlit UI
↓
AI Instruction Generator
↓
Risk Detection Engine
↓
Memory Context Manager
↓
Groq LLM API
↓
Response Output (English + Urdu)



---

## 🧪 Example Use Cases

- “Can I eat rice after discharge?”  
- “When should I take my medicine?”  
- “What should I avoid with high blood pressure?”  
- “Is dizziness normal after medication?”  

---

## 🛠️ Tech Stack

- Python 🐍  
- Streamlit 🎈  
- Groq API 🤖  
- LLaMA Models 🧠  
- python-dotenv 🔐  

---

## 📂 Project Structure
patient-followup-assistant/
│
├── app.py
│   └── Streamlit UI (main entry point)
│
├── core/
│   ├── ai_engine.py
│   │   └── Groq LLM integration + response generation
│   │
│   ├── risk.py
│   │   └── Patient risk detection system
│   │
│   └── memory.py
│       └── Conversation memory management
│
├── data/
│   └── sample_discharge.txt
│       └── Example discharge summary
│
├── requirements.txt
│   └── Project dependencies
│
├── .env
│   └── Environment variables (NOT pushed to GitHub)
│
└── README.md
    └── Project documentation

---

## 🔐 Security Notes

- API keys stored in Streamlit Secrets / .env  
- No patient data is permanently stored  
- Designed for educational and simulation purposes  

---

## 👨‍💻 Author

Built by Subata Khan  
Focused on AI systems, healthcare automation, and applied LLM products.

---

## ⭐ Why This Project Matters

This is not just a chatbot.

It demonstrates:

- Real-world AI system design  
- Healthcare-focused risk logic  
- Multilingual AI communication  
- Production-level deployment experience  
