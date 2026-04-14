def detect_introduction(text):

    triggers = [
        "quero te apresentar",
        "vou te apresentar",
        "deixa eu te apresentar",
        "conheça",
        "essa é"
    ]

    text = text.lower()

    for t in triggers:
        if t in text:
            return True

    return False