# core/prompts.py

DISCHARGE_PROMPT = """
Convert discharge summary into structured medical instructions.

Rules:
- Only bullet points
- No explanation

Format:
- Condition
- Medication
- Diet
- Monitoring
- Warning
"""

URDU_PROMPT = """
Translate medical instructions into Urdu.

Rules:
- Keep structure same
- No extra info
- Simple Urdu only
"""

CHAT_SYSTEM_PROMPT = """
You are a medical assistant helping a discharged patient.
Be short, safe, and clear.
"""