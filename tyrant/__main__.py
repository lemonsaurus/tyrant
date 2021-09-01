import logging

import discord
from discord.ext.commands import Bot, when_mentioned_or

from tyrant import constants
from tyrant.utils.exceptions import MissingToken

log = logging.getLogger(__name__)

# Initialize the bot
bot = Bot(
    command_prefix=when_mentioned_or(constants.Bot.prefix),  # Invoked commands must have this prefix
    activity=discord.Game(name="lemon"),
    case_insensitive=True,
    max_messages=10_000,
)

# Load the extensions we want
bot.load_extension("tyrant.cogs.lemon_stuff")
bot.load_extension("tyrant.cogs.role_assignment")
bot.load_extension("tyrant.cogs.purge")

# Validate the token
token = constants.Bot.token

if token is None:
    raise MissingToken("No token found in the LEMONSAURUS_DISCORD_TOKEN environment variable!")

# Start the bot
log.info(f"🍋🍋 Tyrant operational 🍋🍋")
bot.run(token)
