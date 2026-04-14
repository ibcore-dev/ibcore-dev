# =================================================
# PRIORITY ENGINE — ORION
# Define prioridade cognitiva da conversa
# =================================================

def calculate_priority(intent, emotional_score, active_episode):

    priority = "normal"

    if active_episode:
        return "alta"

    if emotional_score >= 7:
        priority = "alta"

    elif intent == "decisao":
        priority = "media"

    elif intent == "acao":
        priority = "media"

    return priority