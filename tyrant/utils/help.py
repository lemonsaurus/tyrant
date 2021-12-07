from discord import Embed
from discord.ext import commands
from discord.ext.commands import Bot
from tyrant import constants


class TyrantHelp(commands.HelpCommand):
    """Help command for tyrant."""

    def __init__(self):
        super().__init__()

    async def send_bot_help(self, mapping):
        bot = self.context.bot
        help_embed = Embed(
            title="Help",
            description="Tyrant help list.",
            color=constants.Color.yellow,
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
        bot = self.context.bot
        help_embed = Embed(
            title=f"{constants.Bot.prefix}{command.name} [{' | '.join(list(command.aliases))}]",
            description=(
                command.help if command.description == "" else command.description
            ),
            color=constants.Color.yellow,
        )

        await self.get_destination().send(embed=help_embed)

    async def send_error_message(self, error):
        help_embed: Embed = Embed(
            title="Oops!", description=error, color=constants.Color.yellow
        )

        await self.get_destination().send(embed=help_embed)
