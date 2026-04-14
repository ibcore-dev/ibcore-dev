def detect_conversation_depth(user_input, intent, topic):

    text = user_input.lower()

    simple_questions = [
        "funciona",
        "é bom",
        "vale a pena",
        "é possível"
    ]

    analytical_words = [
        "arquitetura",
        "estrutura",
        "modelo",
        "lógica",
        "integração"
    ]

    strategic_words = [
        "escalar",
        "crescer",
        "estratégia",
        "futuro",
        "impacto"
    ]

    decision_words = [
        "qual escolher",
        "qual caminho",
        "qual decisão"
    ]

    if any(word in text for word in simple_questions):
        return "superficial"

    if any(word in text for word in analytical_words):
        return "analitico"

    if any(word in text for word in strategic_words):
        return "estrategico"

    if any(word in text for word in decision_words):
        return "decisorio"

    if intent == "analise":
        return "analitico"

    if intent == "decisao":
        return "decisorio"

    if topic == "projeto":
        return "analitico"

    return "exploratorio"