from http import cookies
from discord.ext.commands import Bot
from discord.ext.commands import Context
from discord.ext import commands
from discord import Embed, errors

from tyrant import constants


class TyrantHelp(commands.HelpCommand):
    """Help command for tyrant."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def send_bot_help(self, mapping):
        bot: Bot = self.context.bot
        help_embed: Embed = Embed(
            title="Help",
            description="Tyrant help list.",
            color=constants.Bot.embed_color,
        )

        for cog_name in bot.cogs:
            cog = bot.cogs[cog_name]
            field_value = ""

            for cmd in cog.walk_commands():
                field_value += f"**{constants.Bot.prefix}{cmd.name}** [{' | '.join(list(cmd.aliases))}]\n"

            if field_value != "":
                help_embed.add_field(name=cog_name, value=field_value, inline=False)

        await self.get_destination().send(embed=help_embed)

    async def send_command_help(self, command: commands.Command):
        bot: Bot = self.context.bot

        for cog_name in bot.cogs:
            cog = bot.cogs[cog_name]
            for cmd in cog.walk_commands():
                if cmd.name == command.name.strip().lower():
                    help_embed = Embed(
                        title=f"{constants.Bot.prefix}{cmd.name} [{' | '.join(list(cmd.aliases))}]",
                        description=(
                            cmd.help if cmd.description == "" else cmd.description
                        ),
                        color=constants.Bot.embed_color,
                    )
                break

        await self.get_destination().send(embed=help_embed)

    async def send_error_message(self, error):
        help_embed: Embed = Embed(
            title="Oops!", description=error, color=constants.Bot.embed_color
        )

        await self.get_destination().send(embed=help_embed)
