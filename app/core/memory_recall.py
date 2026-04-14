import random
import app.core.memory_manager as memory


def recall_personal_memory(username):

    memories = []

    try:

        esposa = memory.get_profile(username, "esposa_profissao")
        profissao = memory.get_profile(username, "profissao")
        projeto = memory.get_profile(username, "projeto_atual")

        if esposa:
            memories.append(
                f"Você comentou que sua esposa trabalha com {esposa}."
            )

        if profissao:
            memories.append(
                f"Você mencionou que trabalha com {profissao}."
            )

        if projeto:
            memories.append(
                f"Você está desenvolvendo {projeto}."
            )

    except Exception:
        pass

    if memories:
        return random.choice(memories)

    return ""