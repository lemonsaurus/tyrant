from discord import AllowedMentions
from discord.ext import commands
from discord.ext.commands import Bot, Cog, Context

from tyrant import constants


class PickTeam(Cog):
    """Command letting the Tyrant pick a team for the user."""

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
        role = constants.ALL_FRUIT_AND_VEG_ROLES[index]

        await ctx.send(
            f"The Tyrant decided that your role will be: <@&{role}>",
            allowed_mentions=AllowedMentions.none()
        )


def setup(bot: Bot) -> None:
    """Called by discord.py to load the extension which will add the above cog."""
    bot.add_cog(PickTeam())
