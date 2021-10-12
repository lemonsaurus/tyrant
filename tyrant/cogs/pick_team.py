from discord import AllowedMentions
from discord.ext import commands
from discord.ext.commands import Bot, Cog, Context
from loguru import logger

from tyrant import constants


class PickTeam(Cog):
    """Command letting the Tyrant pick a team for the user."""

    def __init__(self, bot: Bot):
        """Initialize this cog with the Bot instance."""
        self.bot = bot

    @commands.command(aliases=("team",))
    async def pick(self, ctx: Context):
        """Let the Tyrant pick a fruit or vegetable for you."""
        # We want a sense of randomness from this algorithm so that the chosen
        # roles are evenly spread out, at the same time we want the command to
        # choose the same roles even if invoked twice.
        key = hash(
            ctx.author.display_name +
            ctx.author.discriminator +
            ctx.author.display_avatar.key
        )

        index = key % len(constants.ALL_FRUIT_AND_VEG_ROLES)
        choice = constants.ALL_FRUIT_AND_VEG_ROLES[index]

        if cog := self.bot.get_cog("FruitVsVegetables"):
            await cog.assign_roles(
                ctx.author,
                ctx.guild.get_role(choice),
                ctx.guild.get_role(constants.ROLE_TO_TEAM[choice])
            )
        else:
            # The FruitVsVegetables cog being loaded is a pretty important
            # aspect of this command but we can still recover without it
            logger.warning('Could not assign role because FruitVsVegetables cog is unloaded')

        await ctx.send(
            f"The Tyrant decided that your role will be: <@&{choice}>",
            allowed_mentions=AllowedMentions.none()
        )


def setup(bot: Bot) -> None:
    """Called by discord.py to load the extension which will add the above cog."""
    bot.add_cog(PickTeam(bot))
