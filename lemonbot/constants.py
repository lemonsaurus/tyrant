import os
from typing import Optional


class Bot:
    """Constants relating to the bot itself."""
    token: Optional[str] = os.environ.get("LEMON_DISCORD_TOKEN")
    prefix: str = "!"


class Channels:
    """Channel IDs that are relevant for this community."""
    lemon_spam: int = 718180500568801352


class Roles:
    """Roles relevant to this bot."""
    average_lemon: int = 718181055902908516
    lemon_allies: int = 718216622929739926
