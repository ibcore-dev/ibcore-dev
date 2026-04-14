def determine_focus(topic, emotional_score, intent, active_episode):

    # episódio ativo sempre domina
    if active_episode:
        return "episodio"

    # emoção muito forte domina
    if emotional_score and emotional_score >= 7:
        return "emocional"

    # perguntas focam no tópico
    if intent == "pergunta":
        return topic

    # decisão
    if intent == "decisao":
        return topic

    # ação
    if intent == "acao":
        return "execucao"

    return topic