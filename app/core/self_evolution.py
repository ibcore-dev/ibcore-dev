import re
from app.core.memory_manager import save_profile


# =================================================
# DETECTAR CONHECIMENTO DO USUÁRIO
# =================================================

def extract_user_knowledge(text: str):

    text = text.lower()

    knowledge = {}

    # profissão
    if "trabalho com" in text:
        match = re.search(r"trabalho com ([a-zA-Z\s]+)", text)
        if match:
            knowledge["profissao"] = match.group(1).strip()

    # projetos
    if "projeto" in text:
        if "orion" in text:
            knowledge["projeto"] = "orion"

    # interesses
    if "estou estudando" in text:
        match = re.search(r"estou estudando ([a-zA-Z\s]+)", text)
        if match:
            knowledge["interesse"] = match.group(1).strip()

    return knowledge


# =================================================
# APRENDER COM CONVERSA
# =================================================

def learn_from_conversation(username, text):

    knowledge = extract_user_knowledge(text)

    for key, value in knowledge.items():
        save_profile(username, key, value)

    return knowledge