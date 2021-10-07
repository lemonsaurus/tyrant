import logging
import socket
from typing import Optional

import discord
from aiohttp import AsyncResolver, ClientSession, TCPConnector
from discord.ext import commands

from tyrant import constants

log = logging.getLogger(__name__)


class Tyrant(commands.Bot):
    """Base bot instance."""

    name = "Tyrant"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.http_session: Optional[ClientSession] = None
        self._connector: Optional[TCPConnector] = None

    async def login(self, *args, **kwargs) -> None:
        """Re-create the connector and set up sessions before logging into Discord."""
        # Use asyncio for DNS resolution instead of threads so threads aren't spammed.
        self._connector = TCPConnector(
            resolver=AsyncResolver(),
            family=socket.AF_INET,
        )

        # super() will use this connection for it's internal session.
        self.http.connector = self._connector

        self.http_session = ClientSession(connector=self._connector)

        await super().login(*args, **kwargs)

    async def close(self) -> None:
        """Close http session when bot is shutting down."""
        await super().close()

        if self.http_session:
            await self.http_session.close()
        if self._connector:
            await self._connector.close()

    async def on_ready(self) -> None:
        await self.check_channels()
        await self.send_connection_log()

    def add_cog(self, cog: commands.Cog) -> None:
        """
        Delegate to super to register `cog`.

        This only serves to make the info log, so that extensions don't have to.
        """
        super().add_cog(cog)
        log.info(f"Cog loaded: {cog.qualified_name}")

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

    async def send_connection_log(self) -> None:
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
