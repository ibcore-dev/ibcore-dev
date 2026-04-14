def detect_latent_intent(user_input):

    text = user_input.lower()

    validation_words = [
        "será que",
        "isso funciona",
        "isso dá certo",
        "isso vale"
    ]

    decision_words = [
        "devo",
        "qual escolher",
        "melhor opção",
        "qual é melhor"
    ]

    feasibility_words = [
        "vale a pena",
        "compensa",
        "é viável"
    ]

    insecurity_words = [
        "tenho dúvida",
        "não sei",
        "estou inseguro"
    ]

    for word in validation_words:
        if word in text:
            return "validacao"

    for word in decision_words:
        if word in text:
            return "decisao"

    for word in feasibility_words:
        if word in text:
            return "viabilidade"

    for word in insecurity_words:
        if word in text:
            return "inseguranca"

    return None