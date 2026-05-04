import streamlit as st
from core.ai_engine import safe_ai_call
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

# =========================
# SESSION STATE INIT
# =========================
if "patients" not in st.session_state:
    st.session_state.patients = {}

if "current_patient" not in st.session_state:
    st.session_state.current_patient = None

# =========================
# SAFE PATIENT ACCESS (IMPORTANT FIX)
# =========================
def get_patient():
    name = st.session_state.current_patient
    if name and name in st.session_state.patients:
        return st.session_state.patients[name]
    return None

# =========================
# SIDEBAR
# =========================
st.sidebar.title("🏥 MedAI SaaS Dashboard")

mode = st.sidebar.selectbox("Mode", ["Doctor View", "Admin Analytics"])

# =========================
# ADD PATIENT (FIXED FORM)
# =========================
st.sidebar.subheader("➕ Add Patient")

with st.sidebar.form("add_patient_form"):
    new_name = st.text_input("Name")
    new_age = st.number_input("Age", 0, 120, 30)
    new_condition = st.text_input("Condition")
    new_report = st.text_area("Report")

    submitted = st.form_submit_button("Add Patient")

if submitted:
    if new_name.strip() == "":
        st.sidebar.error("Name is required")
    else:
        st.session_state.patients[new_name] = {
            "name": new_name,
            "age": new_age,
            "condition": new_condition,
            "report": new_report,
            "ai_output": "",
            "chat": []
        }

        st.session_state.current_patient = new_name
        st.sidebar.success(f"Patient '{new_name}' added!")
        st.rerun()

# =========================
# DEMO PATIENT
# =========================
demo_patient = {
    "report": """
BP: 160/100 mmHg

Medications:
- Amlodipine 5mg daily
- Losartan 50mg daily

Diet:
- Low sodium diet

Warning:
- Chest pain
- Dizziness
"""
}

if st.sidebar.button("⚡ Load Demo Patient"):

    st.session_state.patients["Muhammad Ali"] = {
        "name": "Muhammad Ali",
        "age": 58,
        "condition": "Hypertension",
        "report": demo_patient["report"],
        "ai_output": "",
        "chat": []
    }

    st.session_state.current_patient = "Muhammad Ali"
    st.rerun()

# =========================
# PATIENT SELECTOR (FIXED)
# =========================
patient_list = list(st.session_state.patients.keys())

selected_patient = st.sidebar.selectbox(
    "Select Patient",
    patient_list if patient_list else ["No Patients"],
    key="patient_selector"
)

if selected_patient != "No Patients":
    st.session_state.current_patient = selected_patient

# =========================
# LOAD ACTIVE PATIENT
# =========================
patient = get_patient()

# =========================
# HEADER
# =========================
st.title("🏥 MedAI Clinical SaaS Platform")
st.caption("AI-powered hospital discharge + monitoring system")

st.divider()

# =========================
# DOCTOR VIEW
# =========================
if mode == "Doctor View" and patient:

    col1, col2 = st.columns([1, 1])

    # LEFT PANEL
    with col1:
        st.subheader("📄 Patient Record")

        st.info(f"""
👤 {patient['name']}
🎂 Age: {patient['age']}
🩺 Condition: {patient['condition']}
""")

        st.text_area("Medical Report", patient["report"], height=250)

        if st.button("🧠 Generate AI Report"):

            patient = get_patient()

            if patient:
                with st.spinner("AI analyzing..."):

                    prompt = f"""
Convert into structured medical instructions:

{patient['report']}
"""
                    result = safe_ai_call(prompt)

                    st.session_state.patients[patient["name"]]["ai_output"] = result

    # RIGHT PANEL
    with col2:
        st.subheader("📊 Risk Dashboard")

        risk = detect_risk(patient["report"])

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

        st.subheader("🤖 AI Output")

        if patient["ai_output"]:
            st.write(patient["ai_output"])
        else:
            st.info("Generate report first")

    # =========================
    # CHAT
    # =========================
    st.divider()
    st.subheader("💬 AI Assistant Chat")

    msg = st.chat_input("Ask about this patient...")

    if msg:

        patient = get_patient()

        memory = get_memory_context(patient["chat"])

        prompt = f"""
You are a medical assistant.

Patient:
{patient['name']}
Condition:
{patient['condition']}
Report:
{patient['report']}

Memory:
{memory}

Question:
{msg}
"""

        with st.spinner("AI thinking..."):
            answer = safe_ai_call(prompt)

        st.chat_message("user").write(msg)
        st.chat_message("assistant").write(answer)

        update_memory(patient["chat"], msg, answer)

# =========================
# ADMIN ANALYTICS
# =========================
elif mode == "Admin Analytics":

    st.subheader("📊 Hospital Analytics Dashboard")

    total = len(st.session_state.patients)

    high = medium = low = 0

    for p in st.session_state.patients.values():
        r = detect_risk(p["report"])
        if r == "HIGH":
            high += 1
        elif r == "MEDIUM":
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

# =========================
# EMPTY STATE
# =========================
else:
    st.info("👈 Add or select a patient from sidebar to begin")