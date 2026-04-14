import re
from app.core.memory_manager import save_profile


def detect_and_save_specs(username: str, text: str):

    text = text.lower()

    # detectar peso
    peso_match = re.search(r"peso.*?(\d+(\.\d+)?)\s*(kg|g)", text)

    if peso_match:

        peso_valor = peso_match.group(1)
        unidade = peso_match.group(3)

        valor_final = f"{peso_valor}{unidade}"

        save_profile(username, "spec_peso", valor_final)

        return f"Entendido. Vou registrar que o peso está definido como {valor_final}."

    return None