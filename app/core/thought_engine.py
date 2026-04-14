# =================================================
# ORION THOUGHT ENGINE
# =================================================

def generate_thought(topic, intent, emotional_score):

    thought = ""

    # análise emocional
    if emotional_score >= 7:
        thought = "O usuário parece emocionalmente carregado."

    elif emotional_score >= 4:
        thought = "Existe um componente emocional moderado."

    # análise de intenção
    if intent == "decisao":
        thought += " Ele está tentando tomar uma decisão."

    elif intent == "acao":
        thought += " Ele quer executar algo."

    elif intent == "pergunta":
        thought += " Ele busca informação."

    # análise de tema
    if topic == "projeto":
        thought += " O assunto envolve um projeto."

    elif topic == "financeiro":
        thought += " O assunto envolve dinheiro ou negócio."

    return thought