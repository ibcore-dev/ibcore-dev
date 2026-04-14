def analyze_technical_question(user_input):

    text = user_input.lower()

    if "funciona" in text:

        return (
            "Depende do que você quer validar no funcionamento. "
            "Podemos analisar a lógica, a integração entre módulos ou o comportamento final do sistema."
        )

    if "arquitetura" in text:

        return (
            "Para um sistema como o Órion, a melhor abordagem é arquitetura modular. "
            "Separar núcleo cognitivo, memória, decisão e resposta ajuda na escalabilidade."
        )

    if "script" in text or "código" in text:

        return (
            "Para validar um script precisamos verificar três pontos: "
            "estrutura lógica, dependências e integração com outros módulos."
        )

    if "sistema" in text:

        return (
            "Quando analisamos um sistema precisamos observar arquitetura, fluxo de dados "
            "e comunicação entre módulos."
        )

    return None