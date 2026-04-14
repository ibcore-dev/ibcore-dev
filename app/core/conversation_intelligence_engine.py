def detect_pending_question(history):

    if not history:
        return None

    last_ai = None

    for h in reversed(history):

        if isinstance(h, dict):
            ai_response = h.get("response")

        elif isinstance(h, tuple) and len(h) > 0:
            ai_response = str(h[0])

        else:
            ai_response = None

        if ai_response:

            last_ai = ai_response
            break

    if not last_ai:
        return None

    if "?" in last_ai:

        return last_ai

    return None


def interpret_short_answer(user_input):

    text = (user_input or "").strip().lower()

    if len(text.split()) <= 3:
        return True

    return False


def continue_conversation(pending_question, user_input):

    if not pending_question:
        return None

    if not interpret_short_answer(user_input):
        return None

    return f"Entendi. Você respondeu: {user_input}. Vamos continuar a partir disso."