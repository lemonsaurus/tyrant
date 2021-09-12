import os
from typing import Optional

NEGATIVE_REPLIES = [
    "Noooooo!!",
    "Nope.",
    "I'm sorry Dave, I'm afraid I can't do that.",
    "I don't think so.",
    "Not gonna happen.",
    "Out of the question.",
    "Huh? No.",
    "Nah.",
    "Naw.",
    "Not likely.",
    "No way, José.",
    "Not in a million years.",
    "Fat chance.",
    "Certainly not.",
    "NEGATORY.",
    "Nuh-uh.",
    "Not in my house!",
]

POSITIVE_REPLIES = [
    "Yep.",
    "Absolutely!",
    "Can do!",
    "Affirmative!",
    "Yeah okay.",
    "Sure.",
    "Sure thing!",
    "You're the boss!",
    "Okay.",
    "No problem.",
    "I got you.",
    "Alright.",
    "You got it!",
    "ROGER THAT",
    "Of course!",
    "Aye aye, cap'n!",
    "I'll allow it.",
]

ERROR_REPLIES = [
    "Please don't do that.",
    "You have to stop.",
    "Do you mind?",
    "In the future, don't do that.",
    "That was a mistake.",
    "You blew it.",
    "You're bad at computers.",
    "Are you trying to kill me?",
    "Noooooo!!",
    "I can't believe you've done this",
]

LEMON_NOUNS = [
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

LEMON_VERBS = [
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

LEMON_FACTS = [
    "Lemons are native to Asia.",
    "Lemons are a hybrid between a sour orange and a citron.",
    "Lemons are rich in vitamin C.",
    "Lemon trees produce fruit all year round.",
    "Lemon zest, grated rinds, is often used in baking.",
    "Lemon tree leaves can be used to make tea.",
    "The high acidity of lemons make them good cleaning aids.",
    "The most common types of lemons are the Meyer, Eureka, and Lisbon lemons.",
    "The name is said to have derived from an Asian word for “sour fruit”.",
    "Lemons are technically berries.",
    "Historians believe that lemons have been around since first century A.D.",
    "It is believed that they cultivated from the Mediterranean.",
    "There are three common lemons which are Bearss, Eureka and Lisbon.",
    "Lemon trees can produce up to 600 pounds in a year and can grow up to 20 feet tall.",
    "California and Arizona produce 95% of the entire lemon crop.",
    "Today, the British Navy requires all ships to carry enough lemons so that every sailor can have an ounce of juice a day.",
    "An average lemon contains eight seeds.",
    "An average lemon holds three tablespoons of juice.",
    "The juice of a lemon contains 5% of citric acid.",
    "There are roughly fifteen calories in each lemon.",
    "Sprinkling the juice on other fruits can prevent them turning brown.",
    "Lemon juice and hot water is good for a sore throat as it is anti-bacterial.",
    "Lemons used to be so rare that kings used to present them to each other as gifts.",
    "During the California Gold Rush in 1849, miners were willing to pay huge amounts of money for a single lemon.",
    "During the Renaissance, ladies used the juice of a lemon to redden their lips.",
    "For natural highlights in your hair, apply lemon juice daily, for a week.",
    "Wealthy Victorians grew lemons trees in their homes as a sign of prestige and to be a fragrant.",
    "In February and March, Menton in the French Riviera celebrates an annual lemon festival.",
    "Lemon oil is used in unsealed rosewood fingerboards of stringed instruments.",
    "The lemon shark is named for its yellowish skin.",
    "Lemons can prevent scurvy.",
    "To power a flashlight bulb, you need 500 wired lemons to conduct electricity.",
    "The heaviest lemon was 11 pounds, 9.7 ounces in 2003.",
    "Lemon was a common unisex name in the 1900’s.",
]

ALL_FRUIT_AND_VEG_ROLES = [
    883078108457083010, 883078590655258674, 802850922375282698, 816010822777831444,
    882529427962069047, 802889394074681426, 802843500638240789, 843204335793602601,
    802851237837799455, 882360895462846545, 882633463432355882, 883077551927484476,
    883077759985930290, 883078311494963210, 883078871770071051, 883080439231840259,
]

EMOJI_TO_ROLE = {
    "yellow_bell_pepper": 883078108457083010,
    "blue_asparagus": 883078590655258674,
    "pomegranate": 802850922375282698,
    "dragonfruit": 816010822777831444,
    "cabbage": 882529427962069047,
    "radish": 802889394074681426,
    "🍊": 802843500638240789,
    "🍌": 843204335793602601,
    "🥝": 802851237837799455,
    "🫐": 882360895462846545,
    "🍇": 882633463432355882,
    "🌶️": 883077551927484476,
    "🥕": 883077759985930290,
    "🥑": 883078311494963210,
}

EMOJI_TO_TEAM = {
    "🌶️": 883078871770071051,
    "🥕": 883078871770071051,
    "yellow_bell_pepper": 883078871770071051,
    "🥑": 883078871770071051,
    "blue_asparagus": 883078871770071051,
    "cabbage": 883078871770071051,
    "radish": 883078871770071051,

    "pomegranate": 883080439231840259,
    "🍊": 883080439231840259,
    "🍌": 883080439231840259,
    "🥝": 883080439231840259,
    "🫐": 883080439231840259,
    "🍇": 883080439231840259,
    "dragonfruit": 883080439231840259,
}


class Bot:
    """Constants relating to the bot itself."""
    token: Optional[str] = os.environ.get("LEMONSAURUS_DISCORD_TOKEN")
    prefix: str = "."


class Channels:
    """Channel IDs that are relevant for this community."""
    fruit_vs_vegetables: int = 883747003597738005

class Messages:
    """Message IDs that are important."""
    fruit_role_assignment: int = 883854743636705280
    veg_role_assignment: int = 883854721411088405


class Roles:
    """Roles relevant to this bot."""
    lemon: int = 575977761739374592
    radish: int = 802889394074681426
    dragonfruit: int = 816010822777831444
    cabbage: int = 882529427962069047
    grapes: int = 882633463432355882
    blueberry: int = 882360895462846545
    asparagus: int = 883078590655258674
    kiwi: int = 802851237837799455
    avacado: int = 883078311494963210
    yellow_pepper: int = 883078108457083010
    banana: int = 843204335793602601
    tangerine: int = 802843500638240789
    carrot: int = 883077759985930290
    chili_pepper: int = 883077551927484476
    pomegranate: int = 802850922375282698
    team_vegetables: int = 883078871770071051
    team_fruit: int = 883080439231840259


class Users:
    """Users relevant to this bot."""
    lemonsaurus: int = 95872159741644800
