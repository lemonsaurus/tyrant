import logging
from typing import Callable

from discord.ext import commands
from discord.ext.commands import Context

log = logging.getLogger(__name__)


def with_role(*role_ids: int) -> Callable:
    """Returns True if the user has any one of the roles in role_ids."""
    async def predicate(ctx: Context) -> bool:
        """With role checker predicate."""
        if not ctx.guild:  # Return False in a DM
            log.debug(f"{ctx.author} tried to use the '{ctx.command.name}'command from a DM. "
                      "This command is restricted by the with_role decorator. Rejecting request.")
            return False

        for role in ctx.author.roles:
            if role.id in role_ids:
                log.debug(f"{ctx.author} has the '{role.name}' role, and passes the check.")
                return True

        log.debug(f"{ctx.author} does not have the required role to use "
                  f"the '{ctx.command.name}' command, so the request is rejected.")
        return False
    return commands.check(predicate)
