# =================================================
# ORION CONTEXT BRIDGE ENGINE
# =================================================

import app.core.memory_manager as memory


# =================================================
# DETECTAR ENTIDADES TÉCNICAS
# =================================================

TECH_ENTITIES = {
    "peso": ["peso", "kg", "quilo", "massa"],
    "motor": ["motor", "propulsão", "propulsor"],
    "bateria": ["bateria", "energia", "carga"],
    "estrutura": ["estrutura", "chassi", "frame"]
}


def detect_technical_entities(text: str):

    text = (text or "").lower()

    entities = []

    for entity, synonyms in TECH_ENTITIES.items():

        for word in synonyms:

            if word in text:
                entities.append(entity)
                break

    return entities


# =================================================
# PONTE ENTRE INTENÇÃO E MEMÓRIA
# =================================================

def bridge_intent_to_memory(username: str, current_input: str, current_topic: str):

    entities = detect_technical_entities(current_input)

    related_facts = []

    for entity in entities:

        fact = memory.get_profile(username, f"spec_{entity}")

        if fact:
            related_facts.append(
                f"Lembrando que o {entity} está definido como {fact}."
            )

    active_ep = memory.get_active_episode(username)

    if active_ep and current_topic == "projeto":

        _, topic, goal, _, _ = active_ep

        return f"Focando no objetivo do {topic}: {goal}. " + " ".join(related_facts)

    return " ".join(related_facts)