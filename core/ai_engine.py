import time
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

# ✅ Create client ONCE here
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def safe_ai_call(prompt, model="llama-3.1-8b-instant"):
    try:
        start = time.time()

        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )

        end = time.time()
        print(f"⏱ Response time: {round(end-start,2)}s")

        return response.choices[0].message.content

    except Exception as e:
        print("AI Error:", str(e))
        return None