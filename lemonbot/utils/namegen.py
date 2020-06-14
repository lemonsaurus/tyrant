import random

_LEMON_NOUNS = [
    "lemonade",
    "limon",
    "citron",
    "citrus",
    "sourfruit",
    "lime",
    "melon",
    "kiwi",
    "fruit",
    "yellowfruit",
    "lemonfish"
]

_LEMON_VERBS = [
    "demonic",
    "pleasant",
    "citrusy",
    "sour",
    "yellow",
    "round",
    "aromatic",
    "juicy",
    "acidic",
    "fresh",
    "sweet",
    "bitter",
    "pale",
    "plain",
]


def generate_lemon_name():
    if random.random() >= 0.80:
        return f"{' '.join(random.choices(_LEMON_VERBS, k=2))} {random.choice(_LEMON_NOUNS)}"
    else:
        return f"{random.choice(_LEMON_VERBS)} {random.choice(_LEMON_NOUNS)}"
