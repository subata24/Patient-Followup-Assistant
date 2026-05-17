from fastapi import APIRouter
from pydantic import BaseModel

from core.ai_engine import safe_ai_call
from core.risk import detect_risk

router = APIRouter()

class PatientRequest(BaseModel):
    report: str

@router.post("/analyze")
def analyze_patient(data: PatientRequest):

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

    return {
        "risk": risk,
        "ai_output": ai_output
    }