import logging

from discord import Embed
from discord.ext.commands import Bot, Cog, Context, group

from lemonbot.constants import Channels, Users

log = logging.getLogger(__name__)


class Minecraft(Cog):
    """Provide minecraft-related features and info."""

    def __init__(self, bot: Bot):
        """Initialize this cog with the Bot instance."""
        self.bot = bot

    @group(name='minecraft', aliases=('mc', 'lemoncraft'))
    async def minecraft(self, ctx: Context):
        """A group that provides various minecraft info."""
        mc_rules = self.bot.get_channel(Channels.mc_rules)
        mc_chat = self.bot.get_channel(Channels.mc_chat)
        owner_lemon = self.bot.get_user(Users.owner_lemon)

        embed = Embed(
            colour=1416344,
            description=(
                f"This community has a minecraft server, generously hosted by {owner_lemon.mention}! "
                f"Head over to {mc_chat.mention} if you wanna discuss it."
            ),
        )

        embed.set_author(
            name="Minecraft",
            icon_url="https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/i/977e8c4f-1c99-46cd-b070-10cd97086c08/d36qrs5-017c3744-8c94-4d47-9633-d85b991bf2f7.png"
        )
        embed.set_thumbnail(
            url="https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/i/977e8c4f-1c99-46cd-b070-10cd97086c08/d36qrs5-017c3744-8c94-4d47-9633-d85b991bf2f7.png"
        )
        embed.add_field(
            name="IP Adress",
            value="51.81.48.105:25588",
            inline=False,
        )
        embed.add_field(
            name="Version",
            value="1.16",
        )
        embed.add_field(
            name="Plugins",
            value="1 person sleep, auto chest locking, more to come..",
            inline=False,
        )
        embed.add_field(
            name="Rules",
            value=f"See {mc_rules.mention}",
            inline=False,
        )

        await ctx.send(embed=embed)


def setup(bot: Bot) -> None:
    """
    Load the minecraft cog
    """
    bot.add_cog(Minecraft(bot))
    log.info("Cog loaded: Minecraft")
