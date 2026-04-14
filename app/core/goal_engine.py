# =================================================
# ORION GOAL ENGINE
# =================================================

import app.core.memory_manager as memory


def detect_goal(text: str):

    text = (text or "").lower()

    triggers = [
        "quero",
        "meu objetivo",
        "preciso terminar",
        "quero terminar",
        "preciso fazer",
        "vou construir"
    ]

    for trigger in triggers:
        if trigger in text:
            return True

    return False


def extract_goal(text: str):

    text = (text or "").strip()

    return text


def save_goal(username: str, goal_text: str):

    memory.save_profile(username, "active_goal", goal_text)


def get_goal(username: str):

    return memory.get_profile(username, "active_goal")


def goal_response(username: str, text: str):

    if detect_goal(text):

        goal = extract_goal(text)

        save_goal(username, goal)

        return f"Entendido. Vou registrar esse objetivo: {goal}"

    return None