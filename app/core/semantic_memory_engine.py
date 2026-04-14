# =================================================
# ORION SEMANTIC MEMORY ENGINE
# =================================================

SEMANTIC_SYNONYMS = {

    "carro": [
        "automovel",
        "automóvel",
        "veiculo",
        "veículo"
    ],

    "celular": [
        "telefone",
        "smartphone",
        "phone"
    ],

    "casa": [
        "residencia",
        "residência",
        "lar"
    ],

    "trabalho": [
        "emprego",
        "serviço",
        "profissão"
    ]
}


def normalize_semantic_input(text: str):

    text = (text or "").lower()

    for base_word, synonyms in SEMANTIC_SYNONYMS.items():

        for synonym in synonyms:

            if synonym in text:
                text = text.replace(synonym, base_word)

    return text