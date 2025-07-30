import random
import re


def generate_engine_id_candidate(display_name: str, engine_type: str, attempt: int) -> str:
    if display_name != "":
        display_name = sanitize_display_name(display_name)

    if display_name == "":
        display_name = f"new-{engine_type}-engine"

    if attempt == 0:
        return f"{display_name}"

    return f"{display_name}-{random.randint(1000, 9999)}"


def sanitize_display_name(display_name: str) -> str:
    """
    Function sanitizes display name of an engine to be a valid engine id string.

    Args:
        display_name (str): Display name of an engine.
    Returns:
        str: Sanitized display name of an engine.
    """
    # lowercase
    sanitized = display_name.lower()
    # replace all spaces and _ characters with -
    sanitized = sanitized.replace(" ", "-")
    sanitized = sanitized.replace("_", "-")
    # strip of -
    sanitized = sanitized.strip("-")
    # remove non-alphabetic leading characters
    for n in sanitized:
        if n.isalpha():
            break
        sanitized = sanitized[1:]
    # remove non-alphanumeric characters except of -
    sanitized = re.sub(r"[^a-zA-Z0-9-]", "", sanitized)
    # trim if too long, max 63 characters minus 4 for random suffix = 59
    return sanitized[:58]
