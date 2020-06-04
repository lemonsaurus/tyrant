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

    async def assign_roles(self, member) -> None:
        """Assigning roles according to display_name"""
        if member.name != "lemon":
            log.info(f"{member.name} is joining. They are not a lemon, assigning lemon allies role.")
            await member.add_roles(self.lemon_allies_role)
        else:
            log.info(f"{member.name} is joining. They are a lemon, assigning average lemon.")
            await member.add_roles(self.average_lemon_role)

    @Cog.listener()
    async def on_member_join(self, member: Member) -> None:
        """Assign roles to all joining users according to name."""
        await self.assign_roles(member)

    @Cog.listener()
    async def on_member_update(self, _: Member, after: Member) -> None:
        """Assign roles to all deroled users according to name."""
        if self.average_lemon_role not in after.roles and self.lemon_allies_role not in after.roles:
            await self.assign_roles(after)


def setup(bot: Bot) -> None:
    """
    This function is called automatically when this cog is loaded by the bot.

    It's only purpose is to load the cog above, and to pass the Bot instance into it.
    """
    bot.add_cog(RoleAssignment(bot))
    log.info("Cog loaded: RoleAssignment")
