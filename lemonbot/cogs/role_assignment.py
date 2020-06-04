import logging

import discord
from discord import Member
from discord.ext.commands import Bot, Cog

from lemonbot import constants

log = logging.getLogger(__name__)


class RoleAssignment(Cog):
    """Everyone must be named lemon."""

    def __init__(self, bot: Bot):
        """Initialize this cog with the Bot instance."""
        self.bot = bot
        self.average_lemon_role = discord.Object(constants.Roles.average_lemon)
        self.lemon_allies_role = discord.Object(constants.Roles.lemon_allies)

    @Cog.listener()
    async def on_member_join(self, member: Member) -> None:
        """Force nickname for all new users to be 'lemon'"""
        if member.display_name != "lemon":
            log.info(f"{member.display_name} is joining. They are not a lemon, assigning lemon allies role.")
            await member.add_roles(self.lemon_allies_role)
        else:
            log.info(f"{member.display_name} is joining. They are a lemon, assigning average lemon.")
            await member.add_roles(self.average_lemon_role)


def setup(bot: Bot) -> None:
    """
    This function is called automatically when this cog is loaded by the bot.

    It's only purpose is to load the cog above, and to pass the Bot instance into it.
    """
    bot.add_cog(RoleAssignment(bot))
    log.info("Cog loaded: RoleAssignment")
