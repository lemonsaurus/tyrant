from typing import Callable

from discord.ext import commands
from discord.ext.commands import Context
from loguru import logger


def with_role(*role_ids: int) -> Callable:
    """Returns True if the user has any one of the roles in role_ids."""
    async def predicate(ctx: Context) -> bool:
        """With role checker predicate."""
        if not ctx.guild:  # Return False in a DM
            logger.debug(
                "{} tried to use the '{}'command from a DM. "
                "This command is restricted by the with_role decorator. Rejecting request.",
                ctx.author,
                ctx.command.name
            )
            return False

        for role in ctx.author.roles:
            if role.id in role_ids:
                logger.debug("{} has the '{}' role, and passes the check.", ctx.author, role.name)
                return True

        logger.debug(
            "{} does not have the required role to use the '{}' command, so the request is rejected.",
            ctx.author,
            ctx.command.name
        )
        return False
    return commands.check(predicate)
