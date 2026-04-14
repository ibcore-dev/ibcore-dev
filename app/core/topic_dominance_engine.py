def detect_dominant_context(user_input, topic, emotional_score, intent):

    text = user_input.lower()

    technical_words = [
        "arquitetura",
        "sistema",
        "script",
        "código",
        "api",
        "módulo",
        "python",
        "funciona"
    ]

    emotional_words = [
        "preocupado",
        "ansioso",
        "triste",
        "cansado",
        "estressado"
    ]

    decision_words = [
        "decidir",
        "escolher",
        "melhor opção",
        "qual caminho"
    ]

    if any(word in text for word in technical_words):
        return "technical"

    if any(word in text for word in emotional_words) or emotional_score >= 6:
        return "emotional"

    if any(word in text for word in decision_words):
        return "decision"

    if topic == "projeto":
        return "strategic"

    return "general"