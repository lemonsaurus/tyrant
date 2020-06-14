import random

from lemonbot.constants import LEMON_NOUNS, LEMON_VERBS


def generate_lemon_name():
    """Generate a random lemony name."""
    if random.random() >= 0.80:
        return f"{' '.join(random.choices(LEMON_VERBS, k=2))} {random.choice(LEMON_NOUNS)}"
    else:
        return f"{random.choice(LEMON_VERBS)} {random.choice(LEMON_NOUNS)}"
