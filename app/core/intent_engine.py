from app.core.llm_engine import generate_llm_response

def detect_intent(text: str):

    t = text.lower().strip()

    # ===============================
    # SAUDAÇÃO
    # ===============================
    saudacoes = [
        "oi", "olá", "ola", "oie",
        "e aí", "e ai", "fala", "opa", "salve",
        "bom dia", "boa tarde", "boa noite",
        "tudo bem", "tudo certo", "como vai"
    ]

    # 🔥 DETECÇÃO FLEXÍVEL
    for s in saudacoes:
        if s in t:
            return "saudacao"

    # 🔥 SE COMEÇAR COM NOME
    if t.startswith("orion") or t.startswith("órion"):
        return "saudacao"

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