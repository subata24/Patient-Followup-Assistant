from fastapi import APIRouter
from pydantic import BaseModel

from core.ai_engine import safe_ai_call
from core.risk import detect_risk

from backend.database import SessionLocal
from backend.crud import create_patient, get_patients

router = APIRouter()


class PatientRequest(BaseModel):
    name: str
    report: str


@router.post("/analyze")
def analyze_patient(data: PatientRequest):

    db = SessionLocal()

    risk = detect_risk(data.report)

    prompt = f"""
You are a medical AI assistant.

Convert this discharge summary into:
- condition
- medication
- diet advice
- warning signs
- follow-up instructions

Discharge Summary:
{data.report}
"""

    ai_output = safe_ai_call(prompt)

    patient = create_patient(
        db=db,
        name=data.name,
        discharge_summary=data.report,
        risk_level=risk
    )

    db.close()

    return {
        "patient_id": patient.id,
        "risk": risk,
        "ai_output": ai_output
    }


@router.get("/patients")
def read_patients():

    db = SessionLocal()

    patients = get_patients(db)

    db.close()

    return patients