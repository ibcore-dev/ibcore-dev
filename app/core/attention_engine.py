# =================================================
# ORION ATTENTION ENGINE
# =================================================

def calculate_attention(
    topic,
    intent,
    emotional_score,
    active_episode,
    semantic_state
):

    weights = {
        "emocional": 0,
        "execucao": 0,
        "decisao": 0,
        "episodio": 0,
        "exploracao": 0
    }

    # emoção
    if emotional_score:
        weights["emocional"] += emotional_score

    # intenção
    if intent == "acao":
        weights["execucao"] += 6

    if intent == "decisao":
        weights["decisao"] += 6

    if intent == "analise":
        weights["exploracao"] += 4

    # episódio ativo
    if active_episode:
        weights["episodio"] += 7

    # estado semântico
    if semantic_state == "ansiedade":
        weights["emocional"] += 3

    if semantic_state == "duvida":
        weights["exploracao"] += 2

    # escolher foco dominante
    dominant = max(weights, key=weights.get)

    return dominant, weights