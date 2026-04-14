# =================================================
# CONTINUITY ENGINE — ORION
# Mantém continuidade de assunto na conversa
# =================================================

from app.core.context_engine import get_context

def detect_continuity(username, topic, intent):

    try:
        context = get_context(username)
    except Exception:
        context = {}

    last_topic = context.get("assunto")

    continuity = {
        "same_topic": False,
        "topic_shift": False,
        "continuity_score": 0
    }

    if not last_topic:
        return continuity

    if last_topic == topic:
        continuity["same_topic"] = True
        continuity["continuity_score"] = 5
    else:
        continuity["topic_shift"] = True
        continuity["continuity_score"] = 2

    return continuity