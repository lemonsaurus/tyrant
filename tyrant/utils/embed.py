from discord.ext import commands
from discord.ext.commands.context import Context
from discord import Embed

from tyrant import constants


def create_help_embed(ctx: Context, cmd_name: str = None):
    """Creates dynamic embed for help command."""
    if cmd_name is None:
        help_embed = Embed(
            title="Help!",
            description="Tyrant Help list.",
            color=constants.Bot.embed_color,
        )
        for cog_name in ctx.bot.cogs:
            cog = ctx.bot.cogs[cog_name]
            field_value = ""
            for cmd in cog.walk_commands():
                field_value += f"**{constants.Bot.prefix}{cmd.name}** [{' | '.join(list(cmd.aliases))}]\n"

            if field_value != "":
                help_embed.add_field(name=cog_name, value=field_value, inline=True)
        return help_embed

    help_embed = Embed(
        title=f"{cmd_name} not found!",
        description=f"use {constants.Bot.prefix}help for more commands!",
        color=constants.Bot.embed_color,
    )

    for cog_name in ctx.bot.cogs:
        cog = ctx.bot.cogs[cog_name]
        for cmd in cog.walk_commands():
            if cmd.name == cmd_name.strip().lower():
                help_embed = Embed(
                    title=f"{constants.Bot.prefix}{cmd.name} [{' | '.join(list(cmd.aliases))}]",
                    description=(
                        cmd.help if cmd.description == "" else cmd.description
                    ),
                    color=constants.Bot.embed_color,
                )
                break

    return help_embed
