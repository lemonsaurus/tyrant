import logging

from discord import Member
from discord.ext.commands import Bot, Cog

from lemonbot.utils.namegen import generate_lemon_name

log = logging.getLogger(__name__)


class LemonNameForce(Cog):
    """Everyone should have lemony names."""

    def __init__(self, bot: Bot):
        """Initialize this cog with the Bot instance."""
        self.bot = bot

    @Cog.listener()
    async def on_member_join(self, member: Member) -> None:
        """Force nickname for all new users to be more lemony"""
        if member.display_name != "lemon":
            log.info(
                f"{member.display_name} tried to join but is is not named lemon! this I cannot abide. "
                f"changing nickname to something lemony."
            )
            await member.edit(
                nick=generate_lemon_name()
            )


def setup(bot: Bot) -> None:
    """
    This function is called automatically when this cog is loaded by the bot.

    It's only purpose is to load the cog above, and to pass the Bot instance into it.
    """
    bot.add_cog(LemonNameForce(bot))
    log.info("Cog loaded: LemonNameForce")
