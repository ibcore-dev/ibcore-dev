import app.core.memory_manager as memory


# =================================================
# DETECTAR EPISÓDIOS IMPORTANTES
# =================================================

def detect_episode(topic, emotional_score, intent):

    if emotional_score >= 7:
        return "evento_emocional"

    if intent == "decisao":
        return "momento_decisao"

    if topic == "projeto":
        return "progresso_projeto"

    return None


# =================================================
# SALVAR EPISÓDIO
# =================================================

def save_episode(username, topic, emotional_score, intent):

    episode_type = detect_episode(topic, emotional_score, intent)

    if not episode_type:
        return

    memory.save_profile(
        username,
        f"episodio_{episode_type}",
        {
            "topic": topic,
            "emotion": emotional_score,
            "intent": intent
        }
    )


# =================================================
# RECUPERAR EPISÓDIO
# =================================================

def recall_episode(username):

    episode = memory.get_profile(username, "episodio_evento_emocional")

    if episode:
        return episode

    episode = memory.get_profile(username, "episodio_progresso_projeto")

    if episode:
        return episode

    return None