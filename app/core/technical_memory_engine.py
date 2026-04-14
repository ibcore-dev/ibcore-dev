# =================================================
# ORION TECHNICAL MEMORY ENGINE
# =================================================

import app.core.memory_manager as memory


def check_technical_memory(username: str, text: str):

    text = (text or "").lower()

    # PESO
    if "peso" in text:

        peso = memory.get_profile(username, "spec_peso")

        if peso:
            return f"O peso do drone está definido como {peso}."

    return None