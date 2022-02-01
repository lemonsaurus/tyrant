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
            description="Tyrant help list.",
            color=constants.Color.yellow,
        )

        for cog_name in bot.cogs:
            cog = bot.cogs[cog_name]
            cog_commands = await self.filter_commands(cog.get_commands(), sort=True)

            field_value = (
                cog.description
                if cog and (cog.description and (len(cog.description) <= 80))
                else ""
            )
            cmd_list = "```\n"

            for cmd in cog_commands:
                if isinstance(cmd, commands.Group):
                    for sub_cmd in await self.filter_commands(cmd.commands, sort=True):
                        cmd_list += f"\n{self.get_command_signature(sub_cmd)}"
                else:
                    cmd_list += f"\n{self.get_command_signature(cmd)}"

            if len(cog_commands) != 0:
                cmd_list += "\n```"
                help_embed.add_field(
                    name=cog_name, value=f"{field_value}{cmd_list}", inline=False
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

        group_commands = await self.filter_commands(group.commands, sort=True)

        if len(group_commands) == 0:
            await self.send_command_help(group)
            return

        help_embed = Embed(title=f"{group.name.title()} {self.fmt_command_aliases(group, add_parenthesis=True)}", color=constants.Color.yellow)

        msg = (group.help if group.description == "" else group.description)
        msg = msg if len(msg) <= 80 else ''

        for command in group_commands:
            description = (
                command.help if command.description == "" else command.description
            ) + "\n"
            cmd = f"```\n{self.get_command_signature(command)}\n```"

            help_embed.add_field(name=command.name.title(), value=f"{description if len(description) <= 80 else ''}{cmd}", inline=False)

        await self.get_destination().send(embed=help_embed)

    async def send_error_message(self, error):
        """Post error message when an error occurs."""
        help_embed: Embed = Embed(
            title="Oops!", description=error, color=constants.Color.yellow
        )

        await self.get_destination().send(embed=help_embed)
