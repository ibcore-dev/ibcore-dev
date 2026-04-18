from app.core.llm_engine import generate_llm_response

import re
import unicodedata


def normalizar(texto: str):
    texto = texto.lower().strip()

    # remove acentos
    texto = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode("utf-8")

    # remove pontuação
    texto = re.sub(r"[^\w\s]", "", texto)

    return texto


def detect_intent(text: str):

    t = normalizar(text)

    palavras = t.split()
    primeira = palavras[0] if palavras else ""
    
    # ===============================
    # DESPEDIDA
    # ===============================
    despedidas = [
        "tchau", "falou", "ate mais", "até mais",
        "ate", "até", "fui", "vou sair", "flw"
    ]

    if any(d in t for d in despedidas):
        return "despedida"
    
    # ===============================
    # SAUDAÇÃO (PRIORIDADE ALTA)
    # ===============================
    saudacoes = [
        "oi", "ola", "oie",
        "e ai", "fala", "opa", "salve",
        "bom dia", "boa tarde", "boa noite",
        "tudo bem", "tudo certo", "como vai"
    ]

    if primeira in saudacoes or any(s in t for s in saudacoes):
        return "saudacao"

    # ===============================
    # RESPOSTAS CURTAS (EXATAS)
    # ===============================
    positivos = ["sim", "quero", "ok", "ja e", "pode ser", "bora"]
    negativos = ["nao", "nem", "negativo"]
    talvez = ["talvez", "quem sabe", "acho que sim", "acho que nao"]

    # 🔥 comparação por palavra EXATA
    if t in positivos:
        return "positivo"

    if t in negativos:
        return "negativo"

    if t in talvez:
        return "incerto"

    # ===============================
    # PERGUNTA
    # ===============================
    if "?" in text:
        return "pergunta"

    # fallback
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