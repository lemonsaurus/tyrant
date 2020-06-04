import logging

from discord import File
from discord.ext import commands
from discord.ext.commands import Bot, Cog, Context

from lemonbot.assets import FILE_CYCLE

log = logging.getLogger(__name__)


class LemonImage(Cog):
    """Post random lemon images."""

    def __init__(self, bot: Bot):
        """Initialize this cog with the Bot instance."""
        self.bot = bot

    @commands.command()
    async def lemon(self, ctx: Context):
        """Post a random image of a lemon."""
        random_lemon = File(next(FILE_CYCLE))
        await ctx.send(file=random_lemon)


def setup(bot: Bot) -> None:
    """
    This function is called automatically when this cog is loaded by the bot.

    It's only purpose is to load the cog above, and to pass the Bot instance into it.
    """
    bot.add_cog(LemonImage(bot))
    log.info("Cog loaded: LemonImage")
