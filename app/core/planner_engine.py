# =================================================
# ORION PLANNER ENGINE
# =================================================

import app.core.memory_manager as memory


def generate_plan(goal_text: str):

    text = (goal_text or "").lower()

    # plano específico para Orion
    if "orion" in text:

        return [
            "finalizar núcleo cognitivo",
            "integrar memória semântica",
            "implementar goal engine",
            "criar planner engine",
            "desenvolver interface mobile"
        ]

    # plano genérico
    return [
        "definir objetivo principal",
        "dividir em etapas menores",
        "executar primeira etapa",
        "avaliar progresso"
    ]


def get_next_step(username: str):

    goal = memory.get_profile(username, "active_goal")

    if not goal:
        return None

    plan = generate_plan(goal)

    if not plan:
        return None

    return plan[0]


def planner_response(username: str):

    goal = memory.get_profile(username, "active_goal")

    if not goal:
        return None

    plan = generate_plan(goal)

    if not plan:
        return None

    steps = "\n".join([f"{i+1}. {step}" for i, step in enumerate(plan)])

    return f"Para alcançar o objetivo '{goal}', sugiro este plano:\n\n{steps}"