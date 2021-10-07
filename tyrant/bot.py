import logging

import discord
from discord.ext import commands

from tyrant import constants

log = logging.getLogger(__name__)


class Tyrant(commands.Bot):
    """Base bot instance."""

    name = "Tyrant"

    async def on_ready(self) -> None:
        await self.check_channels()
        await self.send_log("Connected!")

    async def check_channels(self) -> None:
        """Verifies that all channel constants refer to channels which exist."""
        if constants.Bot.debug:
            log.info("Skipping Channels Check.")
            return

        all_channels_ids = {channel.id for channel in self.get_all_channels()}
        for name, channel_id in vars(constants.Channels).items():
            if name.startswith("_"):
                continue
            if channel_id not in all_channels_ids:
                log.error(f'Channel "{name}" with ID {channel_id} missing')

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
