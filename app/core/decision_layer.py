def decide_response_mode(user_input, topic, emotional_score, intent):

    text = user_input.lower()

    technical_words = [
        "sistema",
        "arquitetura",
        "funciona",
        "código",
        "script",
        "api",
        "python",
        "módulo"
    ]

    emotional_words = [
        "preocupado",
        "ansioso",
        "triste",
        "cansado"
    ]

    if any(word in text for word in technical_words):
        return "estrategico"

    if any(word in text for word in emotional_words):
        return "reflexivo"

    if intent == "acao":
        return "execucao"

    if intent == "decisao":
        return "diretivo"

    return "normal"