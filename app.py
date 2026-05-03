import streamlit as st
from main import safe_ai_call, client, discharge_text, english_text

st.title("🏥 Post Discharge Patient Assistant")

# memory
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# input box
user_question = st.text_input("Ask a question:")

if user_question:

    st.session_state.chat_history.append(f"Patient: {user_question}")
    memory_context = "\n".join(st.session_state.chat_history[-6:])

    chat_prompt = f"""
You are a medical assistant.

Patient condition:
{discharge_text}

Instructions:
{english_text}

Conversation:
{memory_context}

Question:
{user_question}
"""

    response = safe_ai_call(client, chat_prompt)

    if response:
        st.write("🤖 Assistant:")
        st.write(response)

        st.session_state.chat_history.append(f"Assistant: {response}")