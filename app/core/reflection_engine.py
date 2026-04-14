# =================================================
# REFLECTION ENGINE — ORION
# =================================================

def reflect(topic, intent, emotional_score, continuity):

    reflection = {
        "strategy": "normal",
        "confidence": 5
    }

    if emotional_score >= 7:
        reflection["strategy"] = "emocional"
        reflection["confidence"] = 7

    elif intent == "decisao":
        reflection["strategy"] = "analise"
        reflection["confidence"] = 8

    elif intent == "acao":
        reflection["strategy"] = "execucao"
        reflection["confidence"] = 8

    if continuity.get("same_topic"):
        reflection["confidence"] += 1

    return reflection