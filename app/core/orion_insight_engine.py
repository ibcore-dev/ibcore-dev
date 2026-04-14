# =================================================
# ORION INSIGHT ENGINE
# =================================================

import app.core.memory_manager as memory


def generate_morning_insight(username: str):

    state = memory.get_user_state(username)

    episode = memory.get_active_episode(username)

    if not episode:

        return "Bom dia, Thyago. Sistema online. Algum novo projeto estratégico para hoje?"

    ep_id, topic, goal, decision, phase = episode

    if decision:

        return (
            f"Bom dia. Notei que ainda temos uma decisão sobre "
            f"'{decision}' no projeto {topic}. "
            f"Queremos resolver isso agora para avançar para a fase de {phase}?"
        )

    if phase == "executando":

        return (
            f"Sistema pronto. Continuando a execução do {topic}. "
            f"O foco hoje permanece em: {goal}?"
        )

    return f"Relatório Orion: Projeto {topic} está em fase de {phase}. Pronto para prosseguir."