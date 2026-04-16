from app.conversation.greeting_detector import detect_greeting
from app.conversation.introduction_detector import detect_introduction
from app.conversation.conversation_loop import detect_loop
from app.core.context_bridge_engine import bridge_intent_to_memory
from app.core.spec_learning_engine import detect_and_save_specs


def process_conversation(username, user_input, history):

    loop_response = detect_loop(user_input, history)

    if loop_response:
        return {
            "handled": True,
            "response": loop_response
        }

    text = (user_input or "").lower().strip()

    spec_response = detect_and_save_specs(username, text)

    if spec_response:
        return {
            "handled": True,
            "response": spec_response
        }
    
    
    # 🔥 CONTEXT BRIDGE
    topic = None

    if history:
        last_item = history[-1]

        if isinstance(last_item, dict):
            topic = last_item.get("topic")

        elif isinstance(last_item, tuple):
            topic = None

    context_hint = bridge_intent_to_memory("default_user", user_input, topic)

    # evitar capturar frases que iniciam assunto
    if text.startswith("quero falar") or text.startswith("preciso falar") or text.startswith("vamos falar"):
        return {
            "handled": False,
            "response": None
        }


    # CONTEXT BRIDGE
    topic = None

    if history and isinstance(history[-1], dict):
        topic = history[-1].get("topic")

    context_hint = bridge_intent_to_memory(username, user_input, topic)

    if detect_greeting(text) and len(text.split()) <= 3:
        response = "Olá! Como posso ajudar você hoje?"

        if context_hint:
            response = context_hint + " " + response

        return {
            "handled": True,
            "response": response
        }

    # APRESENTAÇÃO
    if detect_introduction(text):

        response = "Prazer em conhecer! Pode me contar um pouco sobre essa pessoa?"

        if context_hint:
            response = context_hint + " " + response

        return {
            "handled": True,
            "response": response
        }

    return {
        "handled": False,
        "response": context_hint if context_hint else None
    }