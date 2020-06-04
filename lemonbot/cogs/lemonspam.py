import logging

from discord.ext import tasks
from discord.ext.commands import Bot, Cog

from lemonbot import constants

log = logging.getLogger(__name__)


class Lemonspam(Cog):
    """Keep the #sketchbook channel clean, and relay non-sketches to #sketchbook-comments."""

    def __init__(self, bot: Bot):
        """Initialize this cog with the Bot instance."""
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        self.spam_lemon.start()

    @tasks.loop(minutes=1)
    async def spam_lemon(self) -> None:
        """Every minute, spam a lemon into the #lemon-spam channel."""
        await self.bot.get_channel(constants.Channels.lemon_spam).send("lemon")


def setup(bot: Bot) -> None:
    """
    This function is called automatically when this cog is loaded by the bot.

    It's only purpose is to load the cog above, and to pass the Bot instance into it.
    """
    bot.add_cog(Lemonspam(bot))
    log.info("Cog loaded: Lemonspam")
