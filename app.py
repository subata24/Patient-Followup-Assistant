import streamlit as st
from dotenv import load_dotenv
import os

from core.ai_engine import safe_ai_call
from core.risk import detect_risk
from core.memory import add_to_memory, get_memory

load_dotenv()

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="AI Patient Assistant",
    layout="wide"
)

# =========================
# LOAD DATA
# =========================
with open("data/sample_discharge.txt", "r", encoding="utf-8") as f:
    discharge_text = f.read()

# =========================
# SIDEBAR (DASHBOARD)
# =========================
with st.sidebar:
    st.title("🏥 Patient Dashboard")

    st.markdown("### Condition")
    st.info("Hypertension")

    st.markdown("### Risk System")
    st.warning("Auto-detects LOW / MEDIUM / HIGH risk")

    st.markdown("### Instructions Summary")
    st.text(discharge_text[:300])

# =========================
# MAIN UI
# =========================
st.title("🧠 Post-Discharge AI Assistant")

st.markdown("Ask anything about your recovery below 👇")

# =========================
# CHAT HISTORY (UI MEMORY)
# =========================
if "chat" not in st.session_state:
    st.session_state.chat = []

# =========================
# INPUT
# =========================
user_input = st.chat_input("Ask your question...")

if user_input:

    # Save user message
    st.session_state.chat.append(("user", user_input))
    add_to_memory("Patient", user_input)

    # Risk detection
    risk = detect_risk(user_input)

    # Show risk badge
    if risk == "HIGH":
        st.error("⚠️ HIGH RISK DETECTED — Consider contacting doctor")
    elif risk == "MEDIUM":
        st.warning("⚠️ Medium risk — be cautious")
    else:
        st.success("Low risk")

    # Memory context
    memory = get_memory()

    # Prompt
    prompt = f"""
You are a medical assistant.

Patient condition:
{discharge_text}

Conversation:
{memory}

Question:
{user_input}

Be clear, safe, and short.
"""

    # AI CALL
    response = safe_ai_call(prompt)

    # Save assistant response
    st.session_state.chat.append(("assistant", response))
    add_to_memory("Assistant", response)

# =========================
# DISPLAY CHAT (CHATGPT STYLE)
# =========================
for role, msg in st.session_state.chat:

    if role == "user":
        with st.chat_message("user"):
            st.write(msg)

    else:
        with st.chat_message("assistant"):
            st.write(msg)





if st.button("📄 Generate Patient Report"):

    report = f"""
POST DISCHARGE PATIENT REPORT

========================

Condition:
Hypertension

Recent Interaction Summary:
{get_memory()}

Latest Advice:
Follow medication (Amlodipine 5mg daily)
Maintain low sodium diet
Monitor blood pressure regularly

Risk Status:
Auto-detected via system

========================
"""

    st.download_button(
        label="⬇ Download Report",
        data=report,
        file_name="patient_report.txt",
        mime="text/plain"
    )