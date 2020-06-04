import os
from typing import Optional


class Bot:
    """Constants relating to the bot itself."""
    token: Optional[str] = os.environ.get("LEMON_DISCORD_TOKEN")
    prefix: str = "!"


class Channels:
    """Channel IDs that are relevant for this community."""
    lemon_spam: int = 718180500568801352


