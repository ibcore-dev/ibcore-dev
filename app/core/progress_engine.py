# =================================================
# ORION PROGRESS ENGINE
# =================================================

import app.core.memory_manager as memory
from app.core.planner_engine import generate_plan


def get_progress(username: str):

    goal = memory.get_profile(username, "active_goal")

    if not goal:
        return None

    plan = generate_plan(goal)

    if not plan:
        return None

    # progresso salvo
    step_done = memory.get_profile(username, "goal_progress")

    try:
        step_done = int(step_done)
    except:
        step_done = 0

    if step_done >= len(plan):
        return "Objetivo concluído."

    next_step = plan[step_done]

    return f"O próximo passo para '{goal}' é: {next_step}"


def advance_progress(username: str):

    step_done = memory.get_profile(username, "goal_progress")

    try:
        step_done = int(step_done)
    except:
        step_done = 0

    step_done += 1

    memory.save_profile(username, "goal_progress", str(step_done))

    return "Progresso atualizado."