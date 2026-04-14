conversation_context = {}

def update_context(username, user_input):

    text = user_input.lower()

    if username not in conversation_context:
        conversation_context[username] = {}

    ctx = conversation_context[username]

    # =========================
    # CONTEXTO RELACIONAL
    # =========================

    if "minha mãe" in text:
        ctx["pessoa"] = "mãe"

    elif "meu pai" in text:
        ctx["pessoa"] = "pai"

    elif "minha esposa" in text or "minha mulher" in text:
        ctx["pessoa"] = "esposa"

    elif "minha namorada" in text:
        ctx["pessoa"] = "namorada"

    # =========================
    # CONTEXTO DE PROJETO
    # =========================

    if "orion" in text:
        ctx["assunto"] = "orion"
        ctx["ultimo_topico"] = "orion"

    elif any(word in text for word in ["projeto","sistema","codigo","arquitetura"]):
        ctx["ultimo_topico"] = "projeto"

    # =========================
    # SHORT CONTEXT INTERPRETER
    # =========================

    short_patterns = [
        "e a",
        "e o",
        "e os",
        "e as"
    ]

    if any(text.startswith(p) for p in short_patterns):

        last_topic = ctx.get("ultimo_topico")

        if last_topic:

            user_input = f"{user_input} do {last_topic}"

    return ctx


def get_context(username):

    return conversation_context.get(username, {})