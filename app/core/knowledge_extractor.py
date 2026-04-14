# =================================================
# ORION KNOWLEDGE EXTRACTOR
# =================================================

import re
import app.core.memory_manager as memory


def extract_user_knowledge(username: str, text: str):

    text = (text or "").lower()

    knowledge = {}

    # =================================================
    # RELAÇÕES FAMILIARES
    # =================================================

    esposa_match = re.search(r"minha esposa (faz|trabalha com|vende|é) (.+)", text)
    if esposa_match:
        profissao = esposa_match.group(2).strip()
        knowledge["esposa_profissao"] = profissao

    marido_match = re.search(r"meu marido (faz|trabalha com|vende|é) (.+)", text)
    if marido_match:
        profissao = marido_match.group(2).strip()
        knowledge["marido_profissao"] = profissao

    # =================================================
    # PROFISSÃO DO USUÁRIO
    # =================================================

    prof_match = re.search(r"(eu sou|eu trabalho com|eu faço) (.+)", text)
    if prof_match:
        profissao = prof_match.group(2).strip()
        knowledge["profissao"] = profissao

    # =================================================
    # PROJETOS
    # =================================================

    projeto_match = re.search(r"(estou criando|estou fazendo|estou desenvolvendo) (.+)", text)
    if projeto_match:
        projeto = projeto_match.group(2).strip()
        knowledge["projeto_atual"] = projeto

    # =================================================
    # SALVAR NO PERFIL
    # =================================================

    for key, value in knowledge.items():
        memory.save_profile(username, key, value)

    return knowledge