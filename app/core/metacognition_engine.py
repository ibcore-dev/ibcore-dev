def metacognitive_check(topic, intent, emotional_score, thought, continuity):

    analysis = {
        "confidence": 0.8,
        "strategy": "normal",
        "adjustment": None
    }

    # baixa confiança se emoção alta
    if emotional_score and emotional_score >= 7:
        analysis["confidence"] = 0.5
        analysis["strategy"] = "calma"

    # decisão precisa de estrutura
    if intent == "decisao":
        analysis["strategy"] = "estruturar"

    # continuidade ativa
    if continuity:
        analysis["strategy"] = "continuar_contexto"

    # dúvida reduz confiança
    if topic == "geral" and intent == "pergunta":
        analysis["confidence"] = 0.6

    return analysis