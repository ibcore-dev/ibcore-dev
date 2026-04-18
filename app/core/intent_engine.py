from app.core.llm_engine import generate_llm_response

def detect_intent(text: str):

    def detect_intent(text: str):

        t = text.lower().strip()

    # pergunta simples
    if "?" in t:
        return "pergunta"

    # ===============================
    # RESPOSTAS CURTAS (PRIORIDADE MÁXIMA)
    # ===============================
    positivos = ["sim", "quero", "ok", "ja é", "já é", "pode ser", "bora"]
    negativos = ["não", "nao", "nem", "negativo"]
    talvez = ["talvez", "quem sabe", "acho que sim", "acho que não", "acho que nao"]

    # POSITIVO
    for p in positivos:
        if p in t:
            return "positivo"

    # NEGATIVO
    for n in negativos:
        if n in t:
            return "negativo"

    # INCERTO
    for i in talvez:
        if i in t:
            return "incerto"
    # ===============================
    # SAUDAÇÃO
    # ===============================
    saudacoes = [
        "oi", "olá", "ola", "oie",
        "e aí", "e ai", "fala", "opa", "salve",
        "bom dia", "boa tarde", "boa noite",
        "tudo bem", "tudo certo", "como vai"
    ]

    for s in saudacoes:
        if s in t:
            return "saudacao"

    return None

def detect_emotion(text: str):

    t = text.lower()

    if "sono" in t or "cansado" in t or "dormindo" in t:
        return "sono"

    if "triste" in t or "mal" in t:
        return "triste"

    if "feliz" in t or "bom" in t:
        return "positivo"

    return None

def detect_intent_llm(text: str):

    prompt = f"""
Classifique a intenção da mensagem do usuário.

Possíveis intenções:
- hora
- data
- pergunta
- conversa
- ação

Mensagem:
{text}

Responda APENAS com a intenção.
"""

    response = generate_llm_response(prompt)

    if not response:
        return "conversa"

    response = response.strip().lower()

    if "hora" in response:
        return "hora"

    if "data" in response:
        return "data"

    if response in ["pergunta", "ação", "acao", "conversa"]:
        return response

    return "conversa"