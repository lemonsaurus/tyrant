from discord import Embed
from discord.ext import commands
from discord.ext.commands import Bot

from tyrant import constants


class TyrantHelp(commands.HelpCommand):
    """Help command for tyrant."""

    def format_aliases(self, command: commands.Command, add_parenthesis: bool = False):
        """Return a formatted string displaying all the aliases of a command."""
        aliases = " | ".join(command.aliases)

        return f"({aliases})" if add_parenthesis else aliases

    def get_command_signature(self, command, add_aliases: bool = True):
        """Return custom command signature."""
        aliases = (
            self.format_aliases(command, add_parenthesis=True) if add_aliases else ""
        )

        signature = command.signature.replace("[", "<").replace("]", ">")

        if isinstance(command.parent, commands.Group):
            return f"{constants.Bot.prefix}{command.parent.name} {command.name} {signature} {aliases}"

        return f"{constants.Bot.prefix}{command.name} {signature} {aliases}"

    async def send_bot_help(self, mapping):
        """Post Tyrant's help menu."""
        bot = self.context.bot
        help_embed = Embed(
            title="Help",
            description="Available commands",
            color=constants.Color.yellow,
        )

        for cog_name in bot.cogs:  # looping through bot cogs
            cog = bot.cogs[cog_name]
            cog_commands = await self.filter_commands(
                cog.get_commands(), sort=True
            )  # filtering just the commands available to the user

            cog_description = (
                cog.description
                if cog and (cog.description and (len(cog.description) <= 80))
                else ""
            )  # only allowing descriptions lesser than 80 characters

            command_list = (
                "```\n"  # initializing command_list code block with triple backticks
            )

            for command in cog_commands:
                if isinstance(command, commands.Group):  # checking if the command is a command group
                    for sub_command in await self.filter_commands(command.commands, sort=True):
                        command_list += f"\n{self.get_command_signature(sub_command)}"
                else:
                    command_list += f"\n{self.get_command_signature(command)}"

            if len(cog_commands) != 0:
                command_list += "\n```"
                help_embed.add_field(
                    name=cog_name,
                    value=f"{cog_description}{command_list}",
                    inline=False,
                )
            else: # if there are no available commands
                help_embed.add_field(
                    name=cog_name,
                    value=f"{cog_description}\n```\nNo available commands.\n```",
                    inline=False,
                )

        await self.get_destination().send(embed=help_embed)

    async def send_command_help(self, command: commands.Command):
        """Post help for specified command."""
        help_text = command.help if command.description == "" else command.description
        help_embed = Embed(
            title=f"{command.name.title()} {self.format_aliases(command, add_parenthesis=True)}",
            description=f"{help_text}\n```\n{self.get_command_signature(command, add_aliases=False)}\n```",
            color=constants.Color.yellow,
        )

        await self.get_destination().send(embed=help_embed)

    async def send_group_help(self, group: commands.Group):
        """Post help for command groups."""
        group_commands = await self.filter_commands(
            group.commands, sort=True
        )  # filtering commands

        if len(group_commands) == 0:
            await self.send_command_help(group)
            return

        help_embed = Embed(
            title=f"{group.name.title()} {self.format_aliases(group, add_parenthesis=True)}",
            color=constants.Color.yellow,
        )

        for command in group_commands:
            description = (
                command.help if command.description == "" else command.description
            ) + "\n"  # setting description to help attr if description is empty
            description = (
                description if len(description) <= 80 else ""
            )  # only allowing descriptions less than or equal to 80 characters

            command_block = f"```\n{self.get_command_signature(command)}\n```"  # setting command help code block

            help_embed.add_field(
                name=command.name.title(),
                value=f"{description if len(description) <= 80 else ''}{command_block}",
                inline=False,
            )

        await self.get_destination().send(embed=help_embed)

    async def send_error_message(self, error):
        """Post error message when an error occurs."""
        help_embed: Embed = Embed(
            title="Oops!", description=error, color=constants.Color.yellow
        )

        await self.get_destination().send(embed=help_embed)
