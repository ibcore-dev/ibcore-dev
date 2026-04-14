# =================================================
# ORION SEMANTIC ENGINE
# =================================================

SEMANTIC_MAP = {

    "fadiga": [
        "to morto",
        "to acabado",
        "sem energia",
        "exausto",
        "muito cansado",
        "to sem cabeça",
        "to destruido"
    ],

    "ansiedade": [
        "ansioso",
        "muito nervoso",
        "preocupado demais",
        "com medo",
        "tenso",
        "angustiado"
    ],

    "duvida": [
        "não sei",
        "to em dúvida",
        "indeciso",
        "confuso",
        "não tenho certeza"
    ]

}


def detect_semantic_state(text: str):

    text = (text or "").lower()

    for state, expressions in SEMANTIC_MAP.items():

        for exp in expressions:

            if exp in text:
                return state

    return None