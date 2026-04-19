conversation_context = {}

def update_context(username, user_input):

    text = user_input.lower().strip()

    if username not in conversation_context:
        conversation_context[username] = {
            "state": "conversa",
            "intent": "conversa",
            "ultimo_topico": None,
            "assunto": None,
            "pessoa": None
        }

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
    # CONTEXTO DE ASSUNTO
    # =========================

    if "orion" in text:
        ctx["assunto"] = "orion"
        ctx["ultimo_topico"] = "orion"

    elif any(word in text for word in ["projeto", "sistema", "codigo", "arquitetura"]):
        ctx["ultimo_topico"] = "projeto"

    # =========================
    # DETECÇÃO DE ESTADO (NOVA)
    # =========================

    # CRIAÇÃO
    if any(w in text for w in ["post", "texto", "conteudo", "ideia"]):
        ctx["state"] = "criacao"

    # RESOLUÇÃO
    elif any(w in text for w in ["erro", "bug", "problema"]):
        ctx["state"] = "resolucao"

    # EXECUÇÃO
    elif any(w in text for w in ["salva", "cria conta", "abre"]):
        ctx["state"] = "execucao"

    # NÃO derruba estado de criação (🔥 importante)
    if ctx.get("state") == "criacao":
        pass
    else:
        ctx["state"] = ctx.get("state", "conversa")

    # =========================
    # INTENÇÃO (leve)
    # =========================

    intent = "conversa"

    if "?" in text:
        intent = "pergunta"

    elif any(w in text for w in ["me ajuda", "ajuda", "preciso"]):
        intent = "ajuda"

    elif any(w in text for w in ["quero", "vou", "preciso fazer"]):
        intent = "acao"

    ctx["intent"] = intent

    # =========================
    # SHORT CONTEXT (MELHORADO)
    # =========================

    short_patterns = ["e a", "e o", "e os", "e as", "e sobre", "e isso"]

    if any(text.startswith(p) for p in short_patterns):

        last_topic = ctx.get("ultimo_topico")

        if last_topic:
            user_input = f"{user_input} do {last_topic}"
            ctx["expanded_input"] = user_input

    # =========================
    # BLOQUEIO DE SALVAMENTO IMPLÍCITO
    # =========================

    ctx["allow_memory"] = any(w in text for w in ["salva", "lembra", "guarda isso"])

    return ctx


def get_context(username):
    return conversation_context.get(username, {})