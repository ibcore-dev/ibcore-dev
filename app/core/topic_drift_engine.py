def detect_topic_drift(user_input, current_topic):

    text = user_input.lower()

    topic_keywords = {
        "orion": ["orion", "assistente", "ia", "sistema"],
        "tecnologia": ["python", "código", "script", "api", "software"],
        "automotivo": ["carro", "motor", "óleo", "mecânica", "injeção"],
        "financeiro": ["dinheiro", "investimento", "lucro", "renda"],
        "emocional": ["triste", "ansioso", "cansado", "preocupado"]
    }

    for topic, keywords in topic_keywords.items():

        for word in keywords:

            if word in text and topic != current_topic:
                return topic

    return current_topic