from app.core.thought_engine import generate_thought
from app.core.reflection_engine import reflect
from app.core.metacognition_engine import metacognitive_check


def cognitive_loop(topic, intent, emotional_score, continuity):

    thought = generate_thought(topic, intent, emotional_score)

    reflection = reflect(topic, intent, emotional_score, continuity)

    meta = metacognitive_check(
        topic,
        intent,
        emotional_score,
        thought,
        continuity
    )

    return {
        "thought": thought,
        "reflection": reflection,
        "meta": meta
    }