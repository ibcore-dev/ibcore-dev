def calculate_context_weight(
    topic,
    intent,
    emotional_score,
    semantic_intent,
    conversation_depth
):

    weights = {}

    # peso do tópico
    if topic == "projeto":
        weights["topic"] = 3
    elif topic == "tecnico":
        weights["topic"] = 2
    else:
        weights["topic"] = 1

    # peso da intenção
    if intent == "decisao":
        weights["intent"] = 3
    elif intent == "pergunta":
        weights["intent"] = 2
    else:
        weights["intent"] = 1

    # peso emocional
    if emotional_score and emotional_score >= 6:
        weights["emotion"] = 3
    elif emotional_score and emotional_score >= 3:
        weights["emotion"] = 2
    else:
        weights["emotion"] = 1

    # intenção semântica
    if semantic_intent == "escalabilidade":
        weights["semantic"] = 3
    elif semantic_intent == "validacao":
        weights["semantic"] = 2
    else:
        weights["semantic"] = 1

    # profundidade da conversa
    if conversation_depth == "estrategico":
        weights["depth"] = 3
    elif conversation_depth == "analitico":
        weights["depth"] = 2
    else:
        weights["depth"] = 1

    dominant_signal = max(weights, key=weights.get)

    return dominant_signal