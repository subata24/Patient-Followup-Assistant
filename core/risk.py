def detect_risk(text):
    text = text.lower()

    high_risk = ["chest pain", "dizzy", "faint", "breathing", "emergency", "collapse"]
    medium_risk = ["headache", "nausea", "weak", "tired", "uncertain"]

    for w in high_risk:
        if w in text:
            return "HIGH"

    for w in medium_risk:
        if w in text:
            return "MEDIUM"

    return "LOW"