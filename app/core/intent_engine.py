from app.core.llm_engine import generate_llm_response


def detect_intent_llm(text: str):

prompt = f"""
Classifique a intenção da mensagem do usuário.

Possíveis intenções:
- hora (quando quer saber horas)
- data (quando quer saber dia/data)
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

    if response in ["pergunta", "decisao", "acao", "analise", "conversa"]:
        return response

    return "conversa" 