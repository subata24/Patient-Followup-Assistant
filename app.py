import requests
import streamlit as st
from core.risk import detect_risk
from core.memory import get_memory_context, update_memory

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="MedAI SaaS",
    page_icon="🏥",
    layout="wide"
)

API_URL = "http://127.0.0.1:8000"

# =========================
# SESSION STATE
# =========================
if "current_patient" not in st.session_state:
    st.session_state.current_patient = None

if "chat_memory" not in st.session_state:
    st.session_state.chat_memory = {}

# =========================
# FETCH PATIENTS FROM FASTAPI
# =========================
def fetch_patients():
    try:
        response = requests.get(f"{API_URL}/patients")
        return response.json()
    except:
        return []

patients = fetch_patients()

# =========================
# SIDEBAR
# =========================
st.sidebar.title("🏥 MedAI SaaS Dashboard")

mode = st.sidebar.selectbox(
    "Mode",
    ["Doctor View", "Admin Analytics"]
)

# =========================
# ADD PATIENT FORM
# =========================
st.sidebar.subheader("➕ Add Patient")

with st.sidebar.form("add_patient_form"):

    new_name = st.text_input("Name")
    new_age = st.number_input("Age", 0, 120, 30)
    new_condition = st.text_input("Condition")
    new_report = st.text_area("Medical Report")

    submitted = st.form_submit_button("Add Patient")

if submitted:

    try:

        response = requests.post(
            f"{API_URL}/analyze",
            json={
                "name": new_name,
                "report": f"""
Age: {new_age}

Condition:
{new_condition}

Report:
{new_report}
"""
            }
        )

        data = response.json()

        st.session_state.current_patient = new_name

        st.sidebar.success("✅ Patient added successfully!")

        st.rerun()

    except Exception as e:
        st.sidebar.error(f"API Error: {e}")

# =========================
# DEMO PATIENT
# =========================
if st.sidebar.button("⚡ Load Demo Patient"):

    demo_report = """
Patient has severe hypertension.

BP: 170/110

Symptoms:
- Chest pain
- Dizziness

Medication:
- Amlodipine
- Losartan

Diet:
- Low sodium
"""

    requests.post(
        f"{API_URL}/analyze",
        json={
            "name": "Muhammad Ali",
            "report": demo_report
        }
    )

    st.session_state.current_patient = "Muhammad Ali"

    st.rerun()

# =========================
# PATIENT SELECTOR
# =========================
patient_names = [p["name"] for p in patients]

selected_patient = st.sidebar.selectbox(
    "Select Patient",
    patient_names if patient_names else ["No Patients"]
)

if selected_patient != "No Patients":
    st.session_state.current_patient = selected_patient

# =========================
# ACTIVE PATIENT
# =========================
active_patient = None

for p in patients:
    if p["name"] == st.session_state.current_patient:
        active_patient = p
        break

# =========================
# HEADER
# =========================
st.title("🏥 MedAI Clinical SaaS Platform")
st.caption("AI-powered hospital discharge + monitoring system")

st.divider()

# =========================
# DOCTOR VIEW
# =========================
if mode == "Doctor View" and active_patient:

    col1, col2 = st.columns([1, 1])

    # =========================
    # LEFT PANEL
    # =========================
    with col1:

        st.subheader("📄 Patient Record")

        st.info(f"""
👤 {active_patient['name']}
🆔 Patient ID: {active_patient['id']}
""")

        st.text_area(
            "Discharge Summary",
            active_patient["discharge_summary"],
            height=300
        )

    # =========================
    # RIGHT PANEL
    # =========================
    with col2:

        st.subheader("📊 Risk Dashboard")

        risk = active_patient["risk_level"]

        if risk == "HIGH":
            st.error("🔴 HIGH RISK")
            st.progress(90)

        elif risk == "MEDIUM":
            st.warning("🟡 MEDIUM RISK")
            st.progress(60)

        else:
            st.success("🟢 LOW RISK")
            st.progress(25)

        st.divider()

        st.subheader("🤖 AI Medical Instructions")

        if st.button("🧠 Generate AI Instructions"):

            with st.spinner("AI analyzing patient..."):

                ai_prompt = f"""
Convert into structured medical instructions:

{active_patient['discharge_summary']}
"""

                ai_response = requests.post(
                    f"{API_URL}/analyze",
                    json={
                        "name": active_patient["name"],
                        "report": active_patient["discharge_summary"]
                    }
                )

                result = ai_response.json()

                st.write(result["ai_output"])

    # =========================
    # AI CHAT
    # =========================
    st.divider()

    st.subheader("💬 AI Assistant")

    if active_patient["name"] not in st.session_state.chat_memory:
        st.session_state.chat_memory[active_patient["name"]] = []

    msg = st.chat_input("Ask about this patient...")

    if msg:

        memory = get_memory_context(
            st.session_state.chat_memory[active_patient["name"]]
        )

        prompt = f"""
You are a medical AI assistant.

Patient:
{active_patient['name']}

Report:
{active_patient['discharge_summary']}

Conversation Memory:
{memory}

Question:
{msg}
"""

        with st.spinner("AI thinking..."):

            response = requests.post(
                f"{API_URL}/analyze",
                json={
                    "name": active_patient["name"],
                    "report": prompt
                }
            )

            result = response.json()

            answer = result["ai_output"]

        st.chat_message("user").write(msg)
        st.chat_message("assistant").write(answer)

        update_memory(
            st.session_state.chat_memory[active_patient["name"]],
            msg,
            answer
        )

# =========================
# ADMIN ANALYTICS
# =========================
elif mode == "Admin Analytics":

    st.subheader("📊 Hospital Analytics Dashboard")

    total = len(patients)

    high = medium = low = 0

    for p in patients:

        if p["risk_level"] == "HIGH":
            high += 1

        elif p["risk_level"] == "MEDIUM":
            medium += 1

        else:
            low += 1

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Patients", total)
    col2.metric("High Risk", high)
    col3.metric("Low Risk", low)

    st.divider()

    st.bar_chart({
        "High": high,
        "Medium": medium,
        "Low": low
    })

    st.divider()

    st.subheader("📋 Patient Database")

    for p in patients:

        with st.expander(f"{p['name']} — {p['risk_level']}"):

            st.write(p["discharge_summary"])

# =========================
# EMPTY STATE
# =========================
else:

    st.info("👈 Add or select a patient from sidebar")