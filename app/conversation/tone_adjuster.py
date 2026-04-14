import random

def adjust_tone(response):

    prefixes = [
        "Entendi.",
        "Perfeito.",
        "Certo.",
        "Claro."
    ]

    if len(response) < 8:
        return response

    prefix = random.choice(prefixes)

    return f"{prefix} {response}"