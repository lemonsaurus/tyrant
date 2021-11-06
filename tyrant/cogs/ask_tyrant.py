import random

from discord.ext import commands
from discord.ext.commands import Bot, Cog, Context

from tyrant import constants

# Unsuitable responses we need to remove.
UNSUITABLE_RESPONSES = [
    "I'm sorry Dave, I'm afraid I can't do that.",
    "Not gonna happen.",
    "Out of the question.",
    "Can do!",
    "You're the boss!",
    "I got you.",
    "No problem.",
    "You got it!",
]


class AskTyrant(Cog):
    """Provide answers for generic yes or no questions."""

    def __init__(self, bot: Bot):
        """Initialize this cog with the Bot instance."""
        self.bot = bot

        self.negative_replies = list(constants.NEGATIVE_REPLIES)
        self.positive_replies = list(constants.POSITIVE_REPLIES)
        self.uncertain_replies = list(constants.UNCERTAIN_REPLIES)

        # Filtering out unsuitable responses for use here.
        for response in UNSUITABLE_RESPONSES:
            if response in self.negative_replies:
                self.negative_replies.remove(response)
            elif response in self.positive_replies:
                self.positive_replies.remove(response)
            elif response in self.uncertain_replies:
                self.uncertain_replies.remove(response)

    @commands.command(aliases=("8b", "8ball", "pleasesir"))
    async def ask(self, ctx: Context, *, question: str = None):
        """Send random answers to generic yes or no questions."""
        if question is None:
            await ctx.send(
                f'**The Tyrant proclaims**, "You are bad at asking questions"'
            )
            return

        random_response = random.choice(
            self.positive_replies + self.negative_replies + self.uncertain_replies
        )

        if random_response in self.positive_replies:
            response_verb = random.choice(constants.POSITIVE_VERBS)
        elif random_response in self.negative_replies:
            response_verb = random.choice(constants.NEGATIVE_VERBS)
        elif random_response in self.uncertain_replies:
            response_verb = random.choice(constants.UNCERTAIN_VERBS)

        await ctx.send(f'**The Tyrant {response_verb},** "{random_response}"')


def setup(bot: Bot) -> None:
    """Add the cog to the bot."""
    bot.add_cog(AskTyrant(bot))
