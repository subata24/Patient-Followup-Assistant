import os
import time
from groq import Groq

def get_client():
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError("GROQ_API_KEY is missing")

    return Groq(api_key=api_key)


def safe_ai_call(prompt, model="llama-3.1-8b-instant"):
    try:
        client = get_client()  # ✅ created only when needed

        start = time.time()

        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )

        end = time.time()
        print(f"⏱ Response time: {round(end-start,2)}s")

        return response.choices[0].message.content

    except Exception as e:
        print("AI ERROR:", str(e))
        return "⚠️ AI service error. Please try again."