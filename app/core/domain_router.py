def detect_domain(user_input):

    text = user_input.lower()

    domains = {

        "tecnologia": [
            "python",
            "código",
            "script",
            "api",
            "software",
            "arquitetura",
            "sistema"
        ],

        "automotivo": [
            "carro",
            "motor",
            "óleo",
            "injeção",
            "mecânica",
            "radiador",
            "embreagem"
        ],

        "financeiro": [
            "dinheiro",
            "investimento",
            "renda",
            "lucro",
            "ações",
            "criptomoeda"
        ],

        "saude": [
            "dor",
            "febre",
            "remédio",
            "sintoma",
            "doença"
        ]

    }

    for domain, keywords in domains.items():

        for word in keywords:

            if word in text:
                return domain

    return "geral"