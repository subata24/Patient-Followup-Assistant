# =========================
# MEMORY MANAGEMENT
# =========================

def get_memory_context(chat_history, limit=6):
    """
    Returns last N messages as context
    """
    return "\n".join(chat_history[-limit:])


def update_memory(chat_history, user_question, answer):
    """
    Stores conversation in memory
    """
    chat_history.append(f"Patient: {user_question}")
    chat_history.append(f"Assistant: {answer}")