import random


# =================================================
# BANCO DE PERGUNTAS
# =================================================

GENERIC_CURIOSITY = [
    "Mas me conta uma coisa: o que te levou a pensar nisso?",
    "Como você chegou a essa conclusão?",
    "O que está passando pela sua cabeça nesse momento?",
    "Você já vinha pensando nisso antes?",
]

PROJECT_CURIOSITY = [
    "Como está evoluindo esse projeto?",
    "O que tem sido mais desafiador nisso até agora?",
    "Você já conseguiu avançar bem nessa ideia?",
]

EMOTIONAL_CURIOSITY = [
    "O que exatamente está pesando mais para você nisso?",
    "Você consegue identificar o que está causando esse sentimento?",
    "Isso vem acontecendo há algum tempo?",
]

BUSINESS_CURIOSITY = [
    "Esse projeto tem potencial de crescimento?",
    "Você já pensou em como escalar isso?",
]


# =================================================
# ENGINE
# =================================================

def generate_curiosity(topic, emotional_score):

    questions = []

    questions.extend(GENERIC_CURIOSITY)

    if topic == "projeto":
        questions.extend(PROJECT_CURIOSITY)

    if topic == "emocional" or emotional_score >= 6:
        questions.extend(EMOTIONAL_CURIOSITY)

    if topic == "negocio":
        questions.extend(BUSINESS_CURIOSITY)

    if not questions:
        return ""

    if random.random() < 0.35:  # 35% das respostas terão pergunta
        return " " + random.choice(questions)

    return ""