import app.core.memory_manager as memory


def detect_learning_pattern(username):

    history = memory.get_user_state_history(username, 10)

    if not history:
        return None

    question_count = 0
    decision_count = 0
    action_count = 0
    emotional_count = 0

    for topic, mode, emotional_score, intent in history:

        if intent == "pergunta":
            question_count += 1

        if intent == "decisao":
            decision_count += 1

        if intent == "acao":
            action_count += 1

        if emotional_score and emotional_score >= 6:
            emotional_count += 1

    if question_count >= 4:
        return "analitico"

    if decision_count >= 4:
        return "decisor"

    if action_count >= 4:
        return "executor"

    if emotional_count >= 4:
        return "emocional"

    return None