import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    try:
        import streamlit as st
        api_key = st.secrets["GROQ_API_KEY"]
    except:
        pass

if not api_key:
    raise ValueError("GROQ_API_KEY missing")

client = Groq(api_key=api_key)


def safe_ai_call(prompt, model="llama-3.1-8b-instant"):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"AI ERROR: {str(e)}"