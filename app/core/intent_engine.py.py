from app.core.llm_engine import generate_llm_response


def detect_intent_llm(text: str):

    prompt = f"""
Classifique a intenção da frase abaixo em UMA palavra:

Opções:
- pergunta
- decisao
- acao
- analise
- conversa

Frase: "{text}"

Responda apenas com uma palavra.
"""

    response = generate_llm_response(prompt)

    if not response:
        return "conversa"

    response = response.strip().lower()

    if response in ["pergunta", "decisao", "acao", "analise", "conversa"]:
        return response

    return "conversa" 