def detect_goal(history):

    if not history:
        return None

    for h in reversed(history):

        if isinstance(h, dict):
            text = (h.get("input", "") or "").lower()

        elif isinstance(h, tuple) and len(h) > 0:
            text = str(h[0]).lower()

        else:
            text = ""

        if "quero" in text or "preciso" in text or "objetivo" in text:
            return text

    return None