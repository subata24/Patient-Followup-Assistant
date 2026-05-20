# =========================
# MEMORY MANAGEMENT
# =========================

def get_memory_context(chat_history, limit=6):
    """
    Returns last N messages as context
    """
    recent_turns = chat_history[-limit:]

    return "\n".join(
        f"Patient: {turn['user']}\nAssistant: {turn['assistant']}"
        for turn in recent_turns
    )


def update_memory(chat_history, user_question, answer):
    """
    Stores conversation in memory
    """
    chat_history.append({
        "user": user_question,
        "assistant": answer
    })
