import logging
import random
import re
from typing import Optional

from discord import Colour, Embed, Message, TextChannel, User
from discord.ext import commands
from discord.ext.commands import Bot, Cog, Context, group

from tyrant.constants import NEGATIVE_REPLIES, Roles
from tyrant.decorators import with_role

log = logging.getLogger(__name__)

MAX_PURGE = 50


class Purge(Cog):
    """
    A cog that allows messages to be deleted in bulk, while applying various filters.

    You can delete messages sent by a specific user, messages sent by bots, all messages, or messages that match a
    specific regular expression.

    The deleted messages are saved and uploaded to the database via an API endpoint, and a URL is returned which can be
    used to view the messages in the Discord dark theme style.
    """

    def __init__(self, bot: Bot):
        self.bot = bot

    @staticmethod
    async def _clean_messages(
        amount: int,
        ctx: Context,
        bots_only: bool = False,
        user: User = None,
        regex: Optional[str] = None,
    ) -> None:
        """A helper function that does the actual message cleaning."""
        def predicate_bots_only(message: Message) -> bool:
            """Return True if the message was sent by a bot."""
            return message.author.bot

        def predicate_specific_user(message: Message) -> bool:
            """Return True if the message was sent by the user provided in the _clean_messages call."""
            return message.author == user

        def predicate_regex(message: Message) -> bool:
            """Check if the regex provided in _clean_messages matches the message content or any embed attributes."""
            content = [message.content]

            # Add the content for all embed attributes
            for embed in message.embeds:
                content.append(embed.title)
                content.append(embed.description)
                content.append(embed.footer.text)
                content.append(embed.author.name)
                for field in embed.fields:
                    content.append(field.name)
                    content.append(field.value)

            # Get rid of empty attributes and turn it into a string
            content = [attr for attr in content if attr]
            content = "\n".join(content)

            # Now let's see if there's a regex match
            if not content:
                return False
            else:
                return bool(re.search(regex.lower(), content.lower()))

        # Is this an acceptable amount of messages to clean?
        if amount > MAX_PURGE:
            embed = Embed(
                color=Colour(0xcd6d6d),
                title=random.choice(NEGATIVE_REPLIES),
                description=f"You cannot clean more than {MAX_PURGE} messages at a time."
            )
            await ctx.send(embed=embed)
            return

        # Set up the correct predicate
        if bots_only:
            predicate = predicate_bots_only      # Delete messages from bots
        elif user:
            predicate = predicate_specific_user  # Delete messages from specific user
        elif regex:
            predicate = predicate_regex          # Delete messages that match regex
        else:
            predicate = None                     # Delete all messages

        # Delete the invocation first
        await ctx.message.delete()

        # Now let's delete the actual messages with purge.
        await ctx.channel.purge(limit=amount, check=predicate)

    @group(invoke_without_command=True, name="clean", aliases=["purge"])
    @with_role(Roles.lemon)
    async def clean_group(self, ctx: Context) -> None:
        """Commands for cleaning messages in channels."""
        await ctx.send_help(ctx.command)

    @clean_group.command(name="user", aliases=["users"])
    @with_role(Roles.lemon)
    async def clean_user(
        self,
        ctx: Context,
        user: User,
        amount: Optional[int] = 10
    ) -> None:
        """Delete messages posted by the provided user, stop cleaning after traversing `amount` messages."""
        await self._clean_messages(amount, ctx, user=user)

    @clean_group.command(name="all", aliases=["everything"])
    @with_role(Roles.lemon)
    async def clean_all(
        self,
        ctx: Context,
        amount: Optional[int] = 10
    ) -> None:
        """Delete all messages, regardless of poster, stop cleaning after traversing `amount` messages."""
        await self._clean_messages(amount, ctx)

    @clean_group.command(name="bots", aliases=["bot"])
    @with_role(Roles.lemon)
    async def clean_bots(
        self,
        ctx: Context,
        amount: Optional[int] = 10,
        channels: commands.Greedy[TextChannel] = None
    ) -> None:
        """Delete all messages posted by a bot, stop cleaning after traversing `amount` messages."""
        await self._clean_messages(amount, ctx, bots_only=True)

    @clean_group.command(name="regex", aliases=["word", "expression"])
    @with_role(Roles.lemon)
    async def clean_regex(
        self,
        ctx: Context,
        regex: str,
        amount: Optional[int] = 10,
    ) -> None:
        """Delete all messages that match a certain regex, stop cleaning after traversing `amount` messages."""
        await self._clean_messages(amount, ctx, regex=regex)


def setup(bot: Bot) -> None:
    """Load the Purge cog."""
    bot.add_cog(Purge(bot))
