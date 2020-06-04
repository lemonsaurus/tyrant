import logging

from discord import Member
from discord.ext.commands import Bot, Cog

log = logging.getLogger(__name__)


class LemonNameForce(Cog):
    """Everyone must be named lemon."""

    def __init__(self, bot: Bot):
        """Initialize this cog with the Bot instance."""
        self.bot = bot

    @Cog.listener()
    async def on_member_update(self, _: Member, after: Member) -> None:
        """It is not permitted to change the name to something else."""
        if after.display_name != "lemon":
            log.info(f"{after.display_name} is AN UNACCEPTABLE NICKNAME! changing it back to lemon. sweet jesus.")
            await after.edit(
                nick="lemon"
            )

    @Cog.listener()
    async def on_member_join(self, member: Member) -> None:
        """Force nickname for all new users to be 'lemon'"""
        if member.display_name != "lemon":
            log.info(f"{member.display_name} tried to join but is is not named lemon! this I cannot abide. changing to lemon.")
            await member.edit(
                nick="lemon"
            )


def setup(bot: Bot) -> None:
    """
    This function is called automatically when this cog is loaded by the bot.

    It's only purpose is to load the cog above, and to pass the Bot instance into it.
    """
    bot.add_cog(LemonNameForce(bot))
    log.info("Cog loaded: LemonNameForce")
