import time
import os
from dotenv import load_dotenv
from groq import Groq

# =========================
# ENV SETUP
# =========================
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("❌ GROQ_API_KEY not found in .env file")

client = Groq(api_key=api_key)

# =========================
# SAFE AI CALL WRAPPER
# =========================
def safe_ai_call(client, prompt, model="llama-3.1-8b-instant"):
    try:
        start_time = time.time()

        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        end_time = time.time()
        print(f"\n⏱ Response time: {round(end_time - start_time, 2)} seconds")

        return response.choices[0].message.content

    except Exception as e:
        error_msg = str(e).lower()

        print("\n⚠️ ERROR OCCURRED")

        if "token" in error_msg:
            print("🚨 Token limit exceeded. Try shorter input.")

        elif "rate" in error_msg or "quota" in error_msg:
            print("🚨 API limit reached. Waiting 60 seconds...")

            for i in range(60, 0, -1):
                print(f"Retrying in {i}s...", end="\r")
                time.sleep(1)

            return None

        elif "model" in error_msg:
            print("🚨 Model error. Check model name.")

        else:
            print("Unknown error:", error_msg)

        return None


# =========================
# LOAD DATA
# =========================
file_path = "data/sample_discharge.txt"

with open(file_path, "r", encoding="utf-8") as file:
    discharge_text = file.read()

# =========================
# STEP 1: ENGLISH SUMMARY
# =========================
english_prompt = f"""
Convert this discharge summary into STRICT structured medical instructions.

RULES:
- Only bullet points
- No extra explanation
- No emotional sentences
- No paragraphs

FORMAT:
- Condition:
- Medication:
- Diet:
- Monitoring:
- Warning:

TEXT:
{discharge_text}
"""

english_text = safe_ai_call(client, english_prompt)

# =========================
# STEP 2: URDU TRANSLATION
# =========================
urdu_prompt = f"""
Translate the following medical instructions into Urdu.

Rules:
- Keep same structure
- Do NOT add new information
- Use simple Urdu
- Be medically accurate

TEXT:
{english_text}
"""

urdu_text = safe_ai_call(client, urdu_prompt)

# =========================
# OUTPUT
# =========================
print("\n" + "=" * 50)
print("POST DISCHARGE PATIENT ASSISTANT")
print("=" * 50)

print("\n🩺 English Instructions:\n")
print(english_text)

print("\n🩺 Urdu Instructions:\n")
print(urdu_text)

print("\n" + "=" * 50)


# =========================
# CHATBOT MODE
# =========================

def detect_risk(text):
    text = text.lower()

    high_risk_keywords = [
        "chest pain", "faint", "dizzy", "breathing", "emergency",
        "very high bp", "missed medicine", "worse", "collapse"
    ]

    medium_risk_keywords = [
        "headache", "nausea", "weak", "tired", "uncertain",
        "side effect", "not sure"
    ]

    for word in high_risk_keywords:
        if word in text:
            return "HIGH"

    for word in medium_risk_keywords:
        if word in text:
            return "MEDIUM"

    return "LOW"


chat_history = []

while True:
    user_question = input("\nAsk a question (type 'exit' to quit): ")

    if user_question.lower() == "exit":
        break

    # =========================
    # MEMORY UPDATE
    # =========================
    chat_history.append(f"Patient: {user_question}")

    memory_context = "\n".join(chat_history[-6:])

    # =========================
    # RISK CHECK
    # =========================
    risk_level = detect_risk(user_question)
    print(f"\n⚠️ Risk Level: {risk_level}")

    # =========================
    # SYSTEM INSTRUCTION
    # =========================
    if risk_level == "HIGH":
        system_instruction = """
You are a medical assistant.

This is a HIGH RISK situation.

You MUST:
- Warn the patient clearly
- Tell them to contact doctor or emergency services immediately
- Be serious and short
"""
    elif risk_level == "MEDIUM":
        system_instruction = """
You are a medical assistant.

This is a MEDIUM RISK situation.

Give cautious advice and suggest contacting doctor if needed.
"""
    else:
        system_instruction = """
You are a medical assistant.

This is LOW RISK.

Provide normal simple guidance.
"""

    # =========================
    # FINAL PROMPT
    # =========================
    chat_prompt = f"""
{system_instruction}

Patient condition:
{discharge_text}

Instructions:
{english_text}

Conversation history:
{memory_context}

Question:
{user_question}
"""

    # =========================
    # AI CALL
    # =========================
    answer = safe_ai_call(client, chat_prompt)

    if answer:
        print("\n🤖 Assistant:")
        print(answer)

        chat_history.append(f"Assistant: {answer}")
    else:
        print("⚠️ No response received.")