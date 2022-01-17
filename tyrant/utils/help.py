from discord import Embed
from discord.ext import commands
from discord.ext.commands import Bot

from tyrant import constants


class TyrantHelp(commands.HelpCommand):
    """Help command for tyrant."""

    async def send_bot_help(self, mapping):
        """Tyrant's help menu command."""
        bot = self.context.bot
        help_embed = Embed(
            title="Help",
            description="Tyrant help list.",
            color=constants.Color.yellow,
        )
 
        for cog_name in bot.cogs:
            cog = bot.cogs[cog_name]
            field_value = ""

            for cmd in await self.filter_commands(cog.get_commands(), sort=True):
                sub_commands = cmd.__dict__.get('all_commands') # unique property for group commands
                if sub_commands is not None: # if it is a group
                    sub_commands_copy = cmd.__dict__.get('all_commands').copy()

                    for sub_command in sub_commands.values(): # removing aliases from command list
                        for alias in sub_command.aliases:
                            if alias in list(sub_commands.keys()):
                                sub_commands_copy.pop(alias, None)

                    field_value += f"**{cmd.name.title()}** Group [{ '|'.join(list(cmd.aliases)) }]\n"
                    for sub_command in sub_commands_copy.values():
                        field_value += f"***{constants.Bot.prefix}{cmd.name}*** **{sub_command.name}** [{' | '.join(list(sub_command.aliases))}]\n"
                else:
                    field_value += f"**{constants.Bot.prefix}{cmd.name}** [{' | '.join(list(cmd.aliases))}]\n"

            if field_value != "":
                help_embed.add_field(name=cog_name, value=field_value, inline=False)

        await self.get_destination().send(embed=help_embed)

    async def send_command_help(self, command: commands.Command):
        """Post help for specified command."""
        help_embed = Embed(
            title=f"{constants.Bot.prefix}{command.name} [{' | '.join(list(command.aliases))}]",
            description=(
                command.help if command.description == "" else command.description
            ),
            color=constants.Color.yellow,
        )

        await self.get_destination().send(embed=help_embed)

    async def send_group_help(self, group:commands.Group):
        """Post help for command groups."""
        subcommands = group.commands
        if len(subcommands) == 0:
            await self.send_command_help(group)
            return

        commands_ = await self.filter_commands(subcommands, sort=True)
        help_embed = Embed(
            title=f"**{group.name}** Help",
            color=constants.Color.yellow
        )
        message = ""

        for command in commands_:
            message += f"**{constants.Bot.prefix}{group.name} {command.name}** [{' | '.join(list(command.aliases))}]\n"

        help_embed.description = message 
        await self.get_destination().send(embed=help_embed)

    async def send_error_message(self, error):
        """Post error message when an error occurs."""
        help_embed: Embed = Embed(
            title="Oops!", description=error, color=constants.Color.yellow
        )

        await self.get_destination().send(embed=help_embed)
