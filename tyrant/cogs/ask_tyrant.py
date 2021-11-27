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

        self.positive_replies = tuple(self.positive_replies)
        self.negative_replies = tuple(self.negative_replies)
        self.uncertain_replies = tuple(self.uncertain_replies)

        self.verb_lookup = {
            self.positive_replies: constants.POSITIVE_VERBS,
            self.negative_replies: constants.NEGATIVE_VERBS,
            self.uncertain_replies: constants.UNCERTAIN_VERBS,
        }

    @commands.command(aliases=("8b", "8ball", "pleasesir"))
    async def ask(self, ctx: Context, *, question: str = None):
        """Post random answers for YES or NO questions."""
        if question is None:
            await ctx.send(
                f'**The Tyrant proclaims**, "You are bad at asking questions"'
            )
            return

        reply_pool = random.choice(
            (self.positive_replies, self.negative_replies, self.uncertain_replies)
        )

        response_verb = random.choice(self.verb_lookup[reply_pool])
        random_response = random.choice(reply_pool)

        await ctx.send(f'**The Tyrant {response_verb},** "{random_response}"')


def setup(bot: Bot) -> None:
    """Add the cog to the bot."""
    bot.add_cog(AskTyrant(bot))
