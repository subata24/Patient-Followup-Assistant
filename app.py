import html
import os

import requests
import streamlit as st
from dotenv import load_dotenv
from core.memory import get_memory_context, update_memory


st.set_page_config(
    page_title="MedAI Assistant",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

load_dotenv()

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000").rstrip("/")
try:
    API_URL = st.secrets.get("API_URL", API_URL).rstrip("/")
except Exception:
    pass

REQUEST_TIMEOUT = 30


if "current_patient" not in st.session_state:
    st.session_state.current_patient = None

if "current_patient_id" not in st.session_state:
    st.session_state.current_patient_id = None

if "chat_memory" not in st.session_state:
    st.session_state.chat_memory = {}

if "ai_output" not in st.session_state:
    st.session_state.ai_output = {}


st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

#MainMenu, footer {
    visibility: hidden;
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    max-width: 1450px;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #071019 0%, #0F172A 100%);
    border-right: 1px solid #1E293B;
    min-width: 320px !important;
    max-width: 320px !important;
}

section[data-testid="stSidebar"] > div {
    width: 320px !important;
}

[data-testid="stSidebar"] * {
    color: #E2E8F0;
}

.hero {
    background: linear-gradient(135deg,#0F172A,#111827);
    padding: 32px;
    border-radius: 18px;
    margin-bottom: 24px;
    border: 1px solid #1E293B;
}

.hero-title {
    font-size: 34px;
    font-weight: 700;
    color: white;
}

.hero-sub {
    color: #CBD5E1;
    margin-top: 8px;
    font-size: 15px;
}

.live-badge {
    margin-top: 18px;
    display: inline-block;
    background: rgba(16,185,129,0.15);
    color: #6EE7B7;
    padding: 8px 14px;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 600;
}

.live-badge.offline {
    background: rgba(239,68,68,0.15);
    color: #FCA5A5;
}

.card-title {
    font-size: 16px;
    font-weight: 700;
    margin-bottom: 18px;
    color: #0F172A;
}

.stButton > button {
    width: 100%;
    border-radius: 12px;
    border: none;
    background: linear-gradient(135deg,#2563EB,#06B6D4);
    color: white;
    font-weight: 600;
    padding: 12px 18px;
}

.ai-box {
    background: #F8FAFC;
    border: 1px solid #E2E8F0;
    border-radius: 14px;
    padding: 18px;
    line-height: 1.8;
    color: #334155;
}

.empty-box {
    background: white;
    border: 1px dashed #CBD5E1;
    border-radius: 18px;
    padding: 80px 20px;
    text-align: center;
}

.empty-title {
    font-size: 24px;
    font-weight: 700;
    margin-top: 14px;
}

.empty-sub {
    margin-top: 8px;
    color: #64748B;
}

[data-testid="stChatMessage"] {
    border-radius: 14px;
    border: 1px solid #E2E8F0;
    padding: 10px;
}

/* Sidebar Inputs */
.stTextInput input,
.stNumberInput input,
.stTextArea textarea {
    background-color: #0F172A !important;
    color: #FFFFFF !important;
<<<<<<< HEAD
    border: 1px solid #334155 !important;
    border-radius: 10px !important;
    font-size: 15px !important;
}

/* BIGGER & CLEARER TEXTAREA */
.stTextArea textarea {
    min-height: 220px !important;
    line-height: 1.7 !important;
    padding: 14px !important;
    font-size: 15px !important;
}

/* Placeholder */
.stTextInput input::placeholder,
.stTextArea textarea::placeholder {
    color: #94A3B8 !important;
    opacity: 1 !important;
}

/* Focus effect */
.stTextInput input:focus,
.stNumberInput input:focus,
.stTextArea textarea:focus {
    border: 1px solid #3B82F6 !important;
    box-shadow: 0 0 0 1px #3B82F6 !important;
=======
    -webkit-text-fill-color: #FFFFFF !important;
    border: 1px solid #334155 !important;
    border-radius: 10px !important;
    font-size: 15px !important;
    opacity: 1 !important;
>>>>>>> b19ff85 (Fix textarea readability)
}

/* BIGGER & CLEARER TEXTAREA */
.stTextArea textarea {
    min-height: 220px !important;
    line-height: 1.7 !important;
    padding: 14px !important;
    font-size: 15px !important;
}

/* Disabled/read-only textarea text */
.stTextArea textarea:disabled,
.stTextArea textarea[disabled] {
    background-color: #0F172A !important;
    color: #E5E7EB !important;
    -webkit-text-fill-color: #E5E7EB !important;
    opacity: 1 !important;
}

/* Placeholder */
.stTextInput input::placeholder,
.stTextArea textarea::placeholder {
    color: #94A3B8 !important;
    -webkit-text-fill-color: #94A3B8 !important;
    opacity: 1 !important;
}

/* Focus effect */
.stTextInput input:focus,
.stNumberInput input:focus,
.stTextArea textarea:focus {
    border: 1px solid #3B82F6 !important;
    box-shadow: 0 0 0 1px #3B82F6 !important;
}

label {
    color: #E2E8F0 !important;
    font-weight: 500 !important;
}

div[data-baseweb="select"] > div {
    background: #111827 !important;
    color: white !important;
    border: 1px solid #334155 !important;
}

[data-testid="stForm"] {
    background: rgba(15,23,42,0.4);
    padding: 16px;
    border-radius: 14px;
    border: 1px solid #1E293B;
}
</style>
""",
    unsafe_allow_html=True,
)


def fetch_patients():
    try:
        response = requests.get(f"{API_URL}/patients", timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        return response.json(), None
    except requests.RequestException:
        return [], "Backend is not reachable. Check API_URL and confirm the FastAPI service is running."


def fetch_api_status():
    try:
        response = requests.get(f"{API_URL}/health", timeout=10)
        response.raise_for_status()
        return True
    except requests.RequestException:
        return False


patients, api_error = fetch_patients()
api_online = api_error is None and fetch_api_status()


with st.sidebar:
    st.markdown(
        """
    <h1 style='font-size:28px;color:white;margin-bottom:0'>
    🏥 MedAI Assistant
    </h1>
    <p style='color:#94A3B8;margin-top:4px'>
    AI Clinical Intelligence Platform
    </p>
    <hr style='border-color:#1E293B'>
    """,
        unsafe_allow_html=True,
    )

    st.subheader("Add Patient")

    with st.form("add_patient_form"):
        patient_name = st.text_input("Patient Name")
        patient_age = st.number_input("Age", min_value=0, max_value=120, value=30)
        patient_condition = st.text_input("Condition")
        patient_report = st.text_area("Discharge Summary", height=150)
        submitted = st.form_submit_button("Add Patient")

    if submitted and patient_name:
        report_text = f"""
Age: {patient_age}

Condition:
{patient_condition}

Discharge Summary:
{patient_report}
"""

        try:
            response = requests.post(
                f"{API_URL}/patients",
                json={"name": patient_name, "report": report_text},
                timeout=REQUEST_TIMEOUT,
            )
            response.raise_for_status()
            created_patient = response.json()

            st.session_state.current_patient = patient_name
            st.session_state.current_patient_id = created_patient.get("patient_id")
            st.success("Patient added")
            st.rerun()

        except requests.RequestException as e:
            st.error(f"API Error: {e}")

    st.divider()

    if st.button("Load Demo Patient"):
        demo = """
Patient diagnosed with severe hypertension.

Symptoms:
- Chest pain
- Dizziness

Medication:
- Amlodipine
- Losartan
"""

        try:
            response = requests.post(
                f"{API_URL}/patients",
                json={"name": "Muhammad Ali", "report": demo},
                timeout=REQUEST_TIMEOUT,
            )
            response.raise_for_status()
            created_patient = response.json()

            st.session_state.current_patient = "Muhammad Ali"
            st.session_state.current_patient_id = created_patient.get("patient_id")
            st.rerun()

        except requests.RequestException as e:
            st.error(f"API Error: {e}")

    st.divider()
    st.subheader("Patients")

    if patients:
        patient_ids = [p["id"] for p in patients]
        patient_labels = {p["id"]: f"{p['name']} (ID: {p['id']})" for p in patients}

        selected_index = 0
        if st.session_state.current_patient_id in patient_ids:
            selected_index = patient_ids.index(st.session_state.current_patient_id)

        selected_patient_id = st.selectbox(
            "Select Patient",
            patient_ids,
            index=selected_index,
            format_func=lambda patient_id: patient_labels[patient_id],
        )

        st.session_state.current_patient_id = selected_patient_id
        st.session_state.current_patient = patient_labels[selected_patient_id]


badge_class = "live-badge" if api_online else "live-badge offline"
badge_text = "System Online" if api_online else "Backend Offline"

st.markdown(
    f"""
<div class="hero">
<div class="hero-title">Clinical Intelligence Dashboard</div>
<div class="hero-sub">AI-powered discharge intelligence · {len(patients)} patient records available</div>
<div class="{badge_class}">● {badge_text}</div>
</div>
""",
    unsafe_allow_html=True,
)

if api_error:
    st.warning(api_error)

active_patient = next(
    (p for p in patients if p["id"] == st.session_state.current_patient_id),
    None,
)


if not active_patient:
    st.markdown(
        """
    <div class="empty-box">
    <div style="font-size:64px">🩺</div>
    <div class="empty-title">No Patient Selected</div>
    <div class="empty-sub">Add a patient from the sidebar or load the demo patient.</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

else:
    risk = active_patient.get("risk_level", "LOW")

    col_a, col_b = st.columns([4, 1])

    with col_a:
        st.subheader(active_patient["name"])
        st.caption(f"Patient ID: {active_patient['id']}")

    with col_b:
        st.metric("Risk", risk)

    left, right = st.columns([1.15, 1])

    with left:
        st.markdown(
            """
        <div class="card-title">📄 Discharge Summary</div>
        """,
            unsafe_allow_html=True,
        )

        st.text_area(
            "summary",
            value=active_patient.get("discharge_summary", ""),
            height=420,
            label_visibility="collapsed",
            disabled=True,
        )

    with right:
        st.markdown(
            """
        <div class="card-title">🤖 AI Clinical Instructions</div>
        """,
            unsafe_allow_html=True,
        )

        patient_id = active_patient["id"]

        if st.button("Generate AI Instructions"):
            with st.spinner("Analyzing..."):
                try:
                    response = requests.post(
                        f"{API_URL}/analyze",
                        json={"report": active_patient["discharge_summary"]},
                        timeout=REQUEST_TIMEOUT,
                    )
                    response.raise_for_status()
                    output = response.json().get("ai_output", "No output generated.")
                    st.session_state.ai_output[patient_id] = output

                except requests.RequestException as e:
                    st.error(f"API Error: {e}")

        if patient_id in st.session_state.ai_output:
            safe_output = html.escape(st.session_state.ai_output[patient_id]).replace(
                "\n", "<br>"
            )

            st.markdown(
                f"""
            <div class="ai-box">
            {safe_output}
            </div>
            """,
                unsafe_allow_html=True,
            )

    st.divider()
    st.subheader("💬 AI Medical Assistant")

    patient_id = active_patient["id"]
    chat_key = str(patient_id)

    if chat_key not in st.session_state.chat_memory:
        st.session_state.chat_memory[chat_key] = []

    for turn in st.session_state.chat_memory[chat_key]:
        with st.chat_message("user"):
            st.write(turn["user"])

        with st.chat_message("assistant"):
            st.write(turn["assistant"])

    user_message = st.chat_input("Ask about this patient...")

    if user_message:
        memory_context = get_memory_context(st.session_state.chat_memory[chat_key])

        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    f"{API_URL}/chat",
                    json={
                        "patient_id": patient_id,
                        "question": user_message,
                        "memory": memory_context,
                    },
                    timeout=REQUEST_TIMEOUT,
                )
                response.raise_for_status()
                answer = response.json().get("answer", "No response generated.")

            except requests.RequestException as e:
                answer = f"API Error: {e}"

        with st.chat_message("user"):
            st.write(user_message)

        with st.chat_message("assistant"):
            st.write(answer)

        update_memory(
            st.session_state.chat_memory[chat_key],
            user_message,
            answer,
        )
