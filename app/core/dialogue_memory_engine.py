def extract_dialogue_topics(history):

    topics = []

    if not history:
        return topics

    for h in history:

        if isinstance(h, dict):
            topic = h.get("topic")

        elif isinstance(h, tuple) and len(h) > 0:
            topic = h[0]

        else:
            topic = None

        if topic and topic not in topics:
            topics.append(topic)

    return topics


def detect_main_topic(history):

    topics = extract_dialogue_topics(history)

    if not topics:
        return None

    return topics[-1]


# =================================================
# SAFE INPUT EXTRACTION (ANTI-CRASH)
# =================================================

def safe_get_input(h):

    if isinstance(h, dict):
        return (h.get("input") or "").lower().strip()

    elif isinstance(h, tuple) and len(h) > 0:
        return str(h[0]).lower().strip()

    return ""


def conversation_already_answered(history, user_input):

    text = (user_input or "").lower().strip()

    if not history:
        return False

    for h in history:

        previous = safe_get_input(h)

        if not previous:
            continue

        if text in previous or previous in text:
            return True

    return False