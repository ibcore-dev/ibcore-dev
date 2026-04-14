import re
import app.core.memory_manager as memory


def learn_from_user(username, user_input):

    text = user_input.lower()

    patterns = [

        r"meu (\w+) (?:é|e) (?:um|uma)?\s*(\w+)",
        r"minha (\w+) (?:é|e) (?:uma)?\s*(\w+)",
        r"meu (\w+) chama (\w+)",
        r"minha (\w+) chama (\w+)",
        r"eu uso ([\w\.]+)",
    ]

    for pattern in patterns:

        match = re.search(pattern, text)

        if match:

            key = match.group(1)
            value = match.group(2)

            memory.save_profile(username, key, value)


def recall_learned_fact(username, key):

    value = memory.get_profile(username, key)

    if value:
        return value

    return None