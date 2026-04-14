def detect_loop(user_input, history):

    if not history:
        return None

    text = user_input.lower().strip()

    short_responses = [
        "arquitetura",
        "desempenho",
        "codigo",
        "estrutura",
        "sim",
        "não",
        "talvez"
    ]

    # 🔒 PEGAR O ÚLTIMO ITEM COM SEGURANÇA
    last_topic = ""

    last = history[-1]

    if isinstance(last, dict):
        last_topic = last.get("topic", "")

    elif isinstance(last, tuple):
        # Caso seja tuple, você pode adaptar futuramente
        # mas por enquanto evita erro
        last_topic = ""

    # =================================================

    if text in short_responses:

        if last_topic == "projeto":
            return "Entendi. Estamos falando da arquitetura do projeto. Você quer focar em organização do código ou desempenho?"

        if last_topic == "negocio":
            return "Certo. Você quer melhorar crescimento, estrutura ou receita?"

    return None