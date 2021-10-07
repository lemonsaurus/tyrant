import logging

import discord
from discord.ext import commands

from tyrant import constants

log = logging.getLogger(__name__)


class Tyrant(commands.Bot):
    """Base bot instance."""

    name = "Tyrant"

    async def on_ready(self) -> None:
        await self.send_log("Connected!")

    async def send_log(self, details: str) -> None:
        """Send a message to the logs channel."""
        try:
            webhook = await self.fetch_webhook(constants.Webhooks.logs)
        except discord.HTTPException as e:
            log.error(f"Failed to fetch webhook to send connection log: status {e.status}")
        else:
            await webhook.send(
                content=details,
                avatar_url=self.user.display_avatar.url,
                username=self.name,
            )
