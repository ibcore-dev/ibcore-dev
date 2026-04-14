import app.core.memory_manager as memory
from app.core.semantic_memory_engine import normalize_semantic_input


def search_memory(username, user_input):

    # 🔥 normalização semântica
    text = normalize_semantic_input(user_input)

    profile = memory.get_full_profile(username)

    if not profile:
        return None

    for key, value in profile:

        if key in text:
            return f"Você comentou anteriormente que seu {key} é {value}."

    return None