import asyncio

from disnake.ext.commands import Bot, Cog

from tyrant import constants


class FruitVsVegetables(Cog):
    """Assign fruit and vegetable roles."""

    def __init__(self, bot: Bot):
        """Initialize this cog with the Bot instance."""
        self.bot = bot
        self.locks = {}

    @Cog.listener()
    async def on_raw_reaction_add(self, payload):
        """Distribute fruit or vegetable role, when appropriate."""
        if payload.channel_id == constants.Channels.fruit_vs_vegetables:
            # Acquire a lock for this user
            if payload.user_id not in self.locks:
                self.locks[payload.user_id] = asyncio.Lock()
            lock = self.locks[payload.user_id]

            # If it's already locked, just do nothing. The code
            # below will clean up and exit with a clean state.
            if lock.locked():
                return

            async with lock:
                # Get the other info we need
                channel = await self.bot.fetch_channel(payload.channel_id)
                guild = self.bot.get_guild(payload.guild_id)
                member = await guild.fetch_member(payload.user_id)
                emoji = payload.emoji

                # Get the role ID from the emoji
                fruit_role_id = constants.EMOJI_TO_ROLE[emoji.name]
                team_id = constants.EMOJI_TO_TEAM[emoji.name]
                fruit_role = guild.get_role(fruit_role_id)
                team_role = guild.get_role(team_id)

                # Get rid of old roles, assign the new ones
                await member.remove_roles(*[role for role in member.roles if role.id in constants.ALL_FRUIT_AND_VEG_ROLES])
                await member.add_roles(fruit_role, team_role)

                # Finally, remove all other reactions than this one
                fruit_message = await channel.fetch_message(constants.Messages.fruit_role_assignment)
                veg_message = await channel.fetch_message(constants.Messages.veg_role_assignment)
                reactions = fruit_message.reactions + veg_message.reactions

                for reaction in reactions:
                    # Do not remove the reaction we're currently adding
                    if reaction.custom_emoji:
                        if reaction.emoji.name == emoji.name:
                            continue
                    else:
                        if str(emoji) == str(reaction.emoji):
                            continue

                    # Otherwise, remove the emoji.
                    users = await reaction.users().flatten()
                    if member in users:
                        await reaction.remove(member)

    @Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        """Remove fruit and veg roles, when appropriate."""
        if payload.channel_id == constants.Channels.fruit_vs_vegetables:
            # Acquire a lock for this user
            if payload.user_id not in self.locks:
                self.locks[payload.user_id] = asyncio.Lock()
            lock = self.locks[payload.user_id]

            async with lock:
                guild = self.bot.get_guild(payload.guild_id)
                member = await guild.fetch_member(payload.user_id)
                emoji = payload.emoji

                # Get the role ID from the emoji
                fruit_role_id = constants.EMOJI_TO_ROLE[emoji.name]
                team_id = constants.EMOJI_TO_TEAM[emoji.name]
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
