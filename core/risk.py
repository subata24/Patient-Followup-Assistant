import re


def _contains_symptom(text, symptom):
    pattern = rf"\b{re.escape(symptom)}\b"
    match = re.search(pattern, text)
    if not match:
        return False

    nearby_prefix = text[max(0, match.start() - 20):match.start()]
    return not re.search(r"\b(no|not|denies|without|negative for)\s+$", nearby_prefix)


def detect_risk(text):
    text = (text or "").lower()

    high_risk = ["chest pain", "dizzy", "faint", "breathing", "emergency", "collapse"]
    medium_risk = ["headache", "nausea", "weak", "tired", "uncertain"]

    for w in high_risk:
        if _contains_symptom(text, w):
            return "HIGH"

    for w in medium_risk:
        if _contains_symptom(text, w):
            return "MEDIUM"

    return "LOW"
