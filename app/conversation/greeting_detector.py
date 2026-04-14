def detect_greeting(text: str) -> bool:

    if not text:
        return False

    text = text.lower().strip()

    greetings = [
        "oi",
        "ola",
        "olá",
        "eai",
        "e aí",
        "fala",
        "opa",
        "salve",
        "bom dia",
        "boa tarde",
        "boa noite",
        "hey",
        "hello"
    ]

    for greeting in greetings:
        if text.startswith(greeting):
            return True

    return False