import requests
import streamlit as st
from core.memory import get_memory_context, update_memory

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="MedAI Assistant",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

API_URL = "http://127.0.0.1:8000"

# =========================================================
# SESSION STATE
# =========================================================

if "current_patient" not in st.session_state:
    st.session_state.current_patient = None

if "chat_memory" not in st.session_state:
    st.session_state.chat_memory = {}

if "ai_output" not in st.session_state:
    st.session_state.ai_output = {}

# =========================================================
# CSS
# =========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Hide streamlit branding */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

/* Main container */
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    max-width: 1450px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #071019 0%, #0F172A 100%);
    border-right: 1px solid #1E293B;
    min-width: 320px !important;
    max-width: 320px !important;
}

section[data-testid="stSidebar"] > div {
    width: 320px !important;
}

/* Sidebar text */
[data-testid="stSidebar"] * {
    color: #E2E8F0;
}

/* Hero */
.hero {
    background: linear-gradient(135deg,#0F172A,#111827);
    padding: 32px;
    border-radius: 24px;
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

/* Cards */
.card {
    background: white;
    border-radius: 22px;
    padding: 24px;
    border: 1px solid #E2E8F0;
    margin-bottom: 20px;
}

.card-title {
    font-size: 16px;
    font-weight: 700;
    margin-bottom: 18px;
    color: #0F172A;
}

/* Patient strip */
.patient-strip {
    background: linear-gradient(135deg,#F8FAFC,#EFF6FF);
    border: 1px solid #DCE7F7;
    padding: 18px 20px;
    border-radius: 18px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 22px;
}

.patient-name {
    font-size: 18px;
    font-weight: 700;
    color: #0F172A;
}

.patient-id {
    font-size: 12px;
    color: #64748B;
    margin-top: 4px;
}

/* Risk badges */
.risk-high {
    background: #FEF2F2;
    color: #DC2626;
    border: 1px solid #FECACA;
}

.risk-medium {
    background: #FFF7ED;
    color: #EA580C;
    border: 1px solid #FED7AA;
}

.risk-low {
    background: #F0FDF4;
    color: #16A34A;
    border: 1px solid #BBF7D0;
}

.risk-badge {
    padding: 8px 14px;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 700;
}

/* Buttons */
.stButton > button {
    width: 100%;
    border-radius: 14px;
    border: none;
    background: linear-gradient(135deg,#2563EB,#06B6D4);
    color: white;
    font-weight: 600;
    padding: 12px 18px;
}

/* AI box */
.ai-box {
    background: #F8FAFC;
    border: 1px solid #E2E8F0;
    border-radius: 18px;
    padding: 18px;
    line-height: 1.8;
    color: #334155;
}

/* Empty state */
.empty-box {
    background: white;
    border: 1px dashed #CBD5E1;
    border-radius: 24px;
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

/* Chat */
[data-testid="stChatMessage"] {
    border-radius: 16px;
    border: 1px solid #E2E8F0;
    padding: 10px;
}


/* INPUT TEXT COLOR FIX */

.stTextInput input,
.stTextArea textarea,
.stNumberInput input,
div[data-baseweb="select"] input {
    color: #FFFFFF !important;
    background: #111827 !important;
    border: 1px solid #334155 !important;
}

/* Placeholder */
.stTextInput input::placeholder,
.stTextArea textarea::placeholder {
    color: #94A3B8 !important;
}

/* Labels */
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
    border-radius: 18px;
    border: 1px solid #1E293B;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# HELPERS
# =========================================================

def fetch_patients():
    try:
        response = requests.get(f"{API_URL}/patients")
        return response.json()
    except:
        return []

def risk_class(risk):
    if risk == "HIGH":
        return "risk-high"

    if risk == "MEDIUM":
        return "risk-medium"

    return "risk-low"

patients = fetch_patients()

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("""
    <h1 style='font-size:28px;color:white;margin-bottom:0'>
    🏥 MedAI Assistant
    </h1>
    <p style='color:#94A3B8;margin-top:4px'>
    AI Clinical Intelligence Platform
    </p>
    <hr style='border-color:#1E293B'>
    """, unsafe_allow_html=True)

    st.subheader("Add Patient")

    with st.form("add_patient_form"):

        patient_name = st.text_input("Patient Name")

        patient_age = st.number_input(
            "Age",
            min_value=0,
            max_value=120,
            value=30
        )

        patient_condition = st.text_input("Condition")

        patient_report = st.text_area(
            "Discharge Summary",
            height=150
        )

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
            requests.post(
                f"{API_URL}/analyze",
                json={
                    "name": patient_name,
                    "report": report_text
                }
            )

            st.session_state.current_patient = patient_name
            st.success("Patient added")
            st.rerun()

        except Exception as e:
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

        requests.post(
            f"{API_URL}/analyze",
            json={
                "name": "Muhammad Ali",
                "report": demo
            }
        )

        st.session_state.current_patient = "Muhammad Ali"
        st.rerun()

    st.divider()

    st.subheader("Patients")

    if patients:

        patient_names = [p["name"] for p in patients]

        selected_patient = st.selectbox(
            "Select Patient",
            patient_names
        )

        st.session_state.current_patient = selected_patient

# =========================================================
# HERO
# =========================================================

st.markdown(f"""
<div class="hero">

<div class="hero-title">
Clinical Intelligence Dashboard
</div>

<div class="hero-sub">
AI-powered discharge intelligence · {len(patients)} patient records available
</div>

<div class="live-badge">
● System Online
</div>

</div>
""", unsafe_allow_html=True)

# =========================================================
# ACTIVE PATIENT
# =========================================================

active_patient = next(
    (
        p for p in patients
        if p["name"] == st.session_state.current_patient
    ),
    None
)

# =========================================================
# EMPTY STATE
# =========================================================

if not active_patient:

    st.markdown("""
    <div class="empty-box">

    <div style="font-size:64px">
    🩺
    </div>

    <div class="empty-title">
    No Patient Selected
    </div>

    <div class="empty-sub">
    Add a patient from the sidebar or load the demo patient.
    </div>

    </div>
    """, unsafe_allow_html=True)

# =========================================================
# MAIN DASHBOARD
# =========================================================

else:

    risk = active_patient.get("risk_level", "LOW")

    col_a, col_b = st.columns([4, 1])

    with col_a:
        st.subheader(active_patient["name"])
        st.caption(f"Patient ID: {active_patient['id']}")

    with col_b:
        st.metric("Risk", risk)

    left, right = st.columns([1.15, 1])

    # =====================================================
    # LEFT
    # =====================================================

    with left:

        st.markdown("""
        <div class="card-title">
        📄 Discharge Summary
        </div>
        """, unsafe_allow_html=True)

        st.text_area(
            "summary",
            value=active_patient.get("discharge_summary", ""),
            height=420,
            label_visibility="collapsed"
        )

    # =====================================================
    # RIGHT
    # =====================================================

    with right:

        st.markdown("""
        <div class="card-title">
        🤖 AI Clinical Instructions
        </div>
        """, unsafe_allow_html=True)

        patient_id = active_patient["id"]

        if st.button("Generate AI Instructions"):

            with st.spinner("Analyzing..."):

                response = requests.post(
                    f"{API_URL}/analyze",
                    json={
                        "name": active_patient["name"],
                        "report": active_patient["discharge_summary"]
                    }
                )

                output = response.json().get(
                    "ai_output",
                    "No output generated."
                )

                st.session_state.ai_output[patient_id] = output

        if patient_id in st.session_state.ai_output:

            st.markdown(f"""
            <div class="ai-box">
            {st.session_state.ai_output[patient_id]}
            </div>
            """, unsafe_allow_html=True)

    # =====================================================
    # CHAT ASSISTANT
    # =====================================================

    st.divider()

    st.subheader("💬 AI Medical Assistant")

    patient_name = active_patient["name"]

    if patient_name not in st.session_state.chat_memory:
        st.session_state.chat_memory[patient_name] = []

    for turn in st.session_state.chat_memory[patient_name]:

        with st.chat_message("user"):
            st.write(turn["user"])

        with st.chat_message("assistant"):
            st.write(turn["assistant"])

    user_message = st.chat_input(
        "Ask about this patient..."
    )

    if user_message:

        memory_context = get_memory_context(
            st.session_state.chat_memory[patient_name]
        )

        prompt = f"""
You are a clinical AI assistant.

Patient:
{patient_name}

Discharge Summary:
{active_patient['discharge_summary']}

Conversation Memory:
{memory_context}

Question:
{user_message}
"""

        with st.spinner("Thinking..."):

            response = requests.post(
                f"{API_URL}/analyze",
                json={
                    "name": patient_name,
                    "report": prompt
                }
            )

            answer = response.json().get(
                "ai_output",
                "No response generated."
            )

        with st.chat_message("user"):
            st.write(user_message)

        with st.chat_message("assistant"):
            st.write(answer)

        update_memory(
            st.session_state.chat_memory[patient_name],
            user_message,
            answer
        )