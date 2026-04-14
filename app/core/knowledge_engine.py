def generate_knowledge_response(user_input, domain):

    text = user_input.lower()

    if domain == "automotivo":

        # >>> AJUSTE: reconhecer mais variações de vela
        if "vela" in text:
            return "Para trocar a vela do carro normalmente é necessário remover a bobina de ignição, usar uma chave de vela para soltar a vela antiga e instalar a nova com o torque correto."

        # >>> AJUSTE: reconhecer injeção ou injetor
        if "injeção" in text or "injetor" in text:
            return "A injeção eletrônica controla a mistura de combustível e ar usando sensores e a ECU do veículo para melhorar eficiência e desempenho."

        # >>> AJUSTE: detectar falha do motor
        if "motor falhando" in text or "motor falha" in text or "falhando" in text:
            return "Um motor falhando pode indicar problemas nas velas, bobinas de ignição, injetores ou sensores da injeção eletrônica."

    return None