import logging

import discord
from discord.ext.commands import Bot, when_mentioned_or

from lemonbot import constants
from lemonbot.utils.exceptions import MissingToken

log = logging.getLogger(__name__)

# Initialize the bot
bot = Bot(
    command_prefix=when_mentioned_or(constants.Bot.prefix),  # Invoked commands must have this prefix
    activity=discord.Game(name="lemon"),
    case_insensitive=True,
    max_messages=10_000,
)

# Load the extensions we want
bot.load_extension("lemonbot.cogs.lemonspam")

# Validate the token
token = constants.Bot.token

if token is None:
    raise MissingToken("No token found in the LEMON_DISCORD_TOKEN environment variable!")

# Start the bot
log.info(f"== All systems nominal. Bot is go for launch. ==")
bot.run(token)
