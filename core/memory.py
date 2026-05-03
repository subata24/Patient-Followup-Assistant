chat_history = []

def add_to_memory(role, message):
    chat_history.append(f"{role}: {message}")

def get_memory(limit=6):
    return "\n".join(chat_history[-limit:])