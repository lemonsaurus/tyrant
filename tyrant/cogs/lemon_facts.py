import logging
import random

from discord import File
from discord.ext import commands
from discord.ext.commands import Bot, Cog, Context

from tyrant import constants

log = logging.getLogger(__name__)


class LemonFacts(Cog):
    """Post random lemon-related stuff."""

    def __init__(self, bot: Bot):
        """Initialize this cog with the Bot instance."""
        self.bot = bot

    @commands.command(aliases=("lemonfact",))
    async def fact(self, ctx: Context):
        """Post a random fact about lemons."""
        random_fact = random.choice(constants.LEMON_FACTS)
        await ctx.send(random_fact)


def setup(bot: Bot) -> None:
    """
    This function is called automatically when this cog is loaded by the bot.

    It's only purpose is to load the cog above, and to pass the Bot instance into it.
    """
    bot.add_cog(LemonFacts(bot))
