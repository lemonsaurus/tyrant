import logging
import random

from discord import File
from discord.ext import commands
from discord.utils import get
from discord.ext.commands import Bot, Cog, Context

from tyrant import constants

log = logging.getLogger(__name__)

class FruitVsVegetables(Cog):
    """Assign fruit and vegetable roles."""

    def __init__(self, bot: Bot):
        """Initialize this cog with the Bot instance."""
        self.bot = bot

    @Cog.listener()
    async def on_raw_reaction_add(self, payload):
        """Distribute fruit or vegetable role, when appropriate."""
        if payload.channel_id == constants.Channels.fruit_vs_vegetables:
            channel = await self.bot.fetch_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            guild = self.bot.get_guild(payload.guild_id)
            member = await guild.fetch_member(payload.user_id)
            emoji = payload.emoji

            # Get the role ID from the emoji
            fruit_role_id = constants.EMOJI_TO_ROLE[emoji.name]
            team_id = constants.EMOJI_TO_TEAM[emoji.name]
            fruit_role = guild.get_role(fruit_role_id)
            team_role = guild.get_role(team_id)

            # Remove all fruit and veg roles from the member
            for role in member.roles:
                if role.id == team_id:
                    continue
                if role.id in constants.ALL_FRUIT_AND_VEG_ROLES:
                    await member.remove_roles(role)

            # Assign the role
            await member.add_roles(fruit_role, team_role)

    @Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        """Remove fruit and veg roles, when appropriate."""
        if payload.channel_id == constants.Channels.fruit_vs_vegetables:
            channel = await self.bot.fetch_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            guild = self.bot.get_guild(payload.guild_id)
            member = await guild.fetch_member(payload.user_id)
            emoji = payload.emoji

            # Get the role ID from the emoji
            fruit_role_id = constants.EMOJI_TO_ROLE[emoji.name]
            team_id = constants.EMOJI_TO_TEAM[emoji.name]
            fruit_role = guild.get_role(fruit_role_id)
            team_role = guild.get_role(team_id)

            # Remove all fruit and veg roles from the member
            for role in member.roles:
                if role.id == fruit_role_id and role.id in constants.ALL_FRUIT_AND_VEG_ROLES:
                    await member.remove_roles(role, team_role)

def setup(bot: Bot) -> None:
    """
    This function is called automatically when this cog is loaded by the bot.

    It's only purpose is to load the cog above, and to pass the Bot instance into it.
    """
    bot.add_cog(FruitVsVegetables(bot))
    log.info("Cog loaded: Fruit vs Vegetables")
