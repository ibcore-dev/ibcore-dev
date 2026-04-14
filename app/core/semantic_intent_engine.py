def detect_semantic_intent(user_input):

    text = user_input.lower()

    validation_patterns = [
        "isso funciona",
        "isso vai dar certo",
        "isso funciona mesmo",
        "será que funciona",
        "isso presta"
    ]

    scalability_patterns = [
        "isso escala",
        "isso aguenta crescer",
        "isso suporta crescimento",
        "isso vai aguentar muitos usuários"
    ]

    viability_patterns = [
        "isso compensa",
        "vale a pena",
        "isso é viável",
        "isso faz sentido"
    ]

    decision_patterns = [
        "qual escolher",
        "qual caminho",
        "qual opção",
        "o que você faria"
    ]

    for pattern in validation_patterns:
        if pattern in text:
            return "validacao"

    for pattern in scalability_patterns:
        if pattern in text:
            return "escalabilidade"

    for pattern in viability_patterns:
        if pattern in text:
            return "viabilidade"

    for pattern in decision_patterns:
        if pattern in text:
            return "decisao"

    return None