import socket
from typing import Optional

import disnake
from aiohttp import AsyncResolver, ClientSession, TCPConnector
from disnake.ext import commands

from loguru import logger

from tyrant import constants
from tyrant.utils import github
from tyrant.utils.help import TyrantHelp


class Tyrant(commands.Bot):
    """Base bot instance."""

    name = "Tyrant"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(
            *args,
            **kwargs,
            help_command=TyrantHelp(),
        )

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
        logger.info("Cog loaded: {}", cog.qualified_name)

    async def check_channels(self) -> None:
        """Verifies that all channel constants refer to channels which exist."""
        if constants.Bot.debug:
            logger.info("Skipping Channels Check.")
            return

        all_channels_ids = {channel.id for channel in self.get_all_channels()}
        for name, channel_id in vars(constants.Channels).items():
            if name.startswith("_"):
                continue
            if channel_id not in all_channels_ids:
                logger.error('Channel "{}" with ID {} missing', name, channel_id)

    async def send_connection_log(self) -> None:
        """Send a message to the logs channel."""
        # stop early if the webhook is not configured
        if not constants.Webhooks.logs:
            logger.info("Connection log webhook is not configured. Unable to send message.")
            return
        try:
            webhook = await self.fetch_webhook(constants.Webhooks.logs)
        except disnake.HTTPException as e:
            logger.error("Failed to fetch webhook to send connection log: status {}", e.status)
        else:
            image_url = await github.get_random_connection_image(self.http_session)
            embed = disnake.Embed(colour=disnake.Colour.dark_magenta(),)
            embed.set_image(url=image_url)
            embed.set_footer(text=f"Version: {constants.Bot.git_sha}")
            await webhook.send(
                embed=embed,
                avatar_url=self.user.display_avatar.url,
                username=self.name,
            )
