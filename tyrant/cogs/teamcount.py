from io import BytesIO
from typing import Union

from disnake import File, Embed
from disnake.ext import commands
from disnake.ext.commands import Bot, Cog, Context

from PIL import Image, ImageFont, ImageDraw, ImageColor

from tyrant import constants
from tyrant.constants import Images, Fonts


class TeamCount(Cog):
    """Provide the current number of members in each team."""

    def __init__(self, bot: Bot):
        """Intialize the cog with the Bot instance."""
        self.bot = bot

    @commands.command(aliases=["fruitsvsveg"])
    async def teamcount(self, ctx: Context):
        """Post a formatted image with the member count in each team."""
        member_count = await self.get_member_count()
        banner_image = await self._create_banner(
            team_vegetable_count=member_count[0], team_fruit_count=member_count[1]
        )

        with BytesIO() as image_binary:
            banner_image.save(
                image_binary, "PNG"
            )  # converting PIL.Image object to binary
            image_binary.seek(0)

            embed = await self._create_banner_embed(ctx=ctx, image=image_binary)

            await ctx.send(embed=embed)

    async def get_member_count(self):
        """Return the current member count from each teams."""
        guild = self.bot.get_guild(constants.Bot.guild)

        team_vegetable_member_count = str(
            len(guild.get_role(constants.Roles.team_vegetables).members)
        )
        team_fruit_member_count = str(
            len(guild.get_role(constants.Roles.team_fruit).members)
        )

        return (team_vegetable_member_count, team_fruit_member_count)

    async def _create_banner_embed(self, ctx: Context, image):
        """Create an embed with the banner image."""
        embed = Embed(color=constants.Color.yellow)
        embed.set_image(file=File(fp=image, filename="teamcount.png"))
        embed.set_footer(
            text=f"Requested by {ctx.author.display_name}",
            icon_url=ctx.author.display_avatar,
        )

        return embed

    async def _create_banner(self, team_vegetable_count: int, team_fruit_count: int):
        """Create banner with the count of members in each team."""
        base_image = Image.open(Images.teamcount_base.resolve().__str__()).convert(
            "RGBA"
        )  # base image object

        shadow = Image.new(
            "RGBA", base_image.size
        )  # image object with base image size for shadows

        self.width = base_image.width
        self.height = base_image.height

        cartonix_font_small = ImageFont.truetype(
            font=Fonts.carton_six.resolve().__str__(), size=70
        )
        cartonix_font_large = ImageFont.truetype(
            font=Fonts.carton_six.resolve().__str__(), size=150
        )

        draw_base = ImageDraw.Draw(base_image)
        draw_shadow = ImageDraw.Draw(shadow)

        team_vegetable_count_x_y = self._get_text_coordinates(
            team="vegetables", member_count=team_vegetable_count
        )
        team_fruit_count_x_y = self._get_text_coordinates(
            team="fruits", member_count=team_fruit_count
        )

        # creating shadow
        draw_shadow.text(
            (self.width / 2 - 17, self.height / 3 + 3),
            "VS",
            fill=(0, 0, 0, 135),
            font=cartonix_font_small,
        )  # adding "vs" text shadow

        draw_shadow.text(
            team_vegetable_count_x_y[0],
            team_vegetable_count,
            fill=(0, 0, 0, 135),
            font=cartonix_font_large,
        )  # adding team vegetable member count shadow

        draw_shadow.text(
            team_fruit_count_x_y[0],
            team_fruit_count,
            fill=(0, 0, 0, 135),
            font=cartonix_font_large,
        )  # adding team fruit member count shadow

        base_image.paste(shadow, shadow)  # paste shadow to base image

        # drawing member count text over shadows
        draw_base.text(
            (self.width / 2 - 20, self.height / 3),
            "VS",
            fill=(255, 255, 255, 255),
            font=cartonix_font_small,
        )  # adding "vs" text

        draw_base.text(
            team_vegetable_count_x_y[1],
            team_vegetable_count,
            fill=ImageColor.getrgb("#80fdd2"),
            font=cartonix_font_large,
        )  # adding team vegetable member count

        draw_base.text(
            team_fruit_count_x_y[1],
            team_fruit_count,
            fill=ImageColor.getrgb("#fcc7f6"),
            font=cartonix_font_large,
        )  # adding team fruit member count

        base_image.show()
        return base_image

    def _get_text_coordinates(self, team: str, member_count: str):
        """Get Coordinates for member_count text according to its length."""

        coordinates = [
            [0, 0],  # coordinates for text shadow
            [0, 0],  # coordinates for main text
        ]

        # The coordinates used below are tested values.
        if team == "fruits":
            if len(member_count) == 1:
                coordinates[0] = [self.width / 3 + 54, 3]
                coordinates[1] = [self.width / 3 + 50, 0]

            if len(member_count) == 2:
                coordinates[0] = [self.width / 3 - 10, 3]
                coordinates[1] = [self.width / 3 - 14, 0]

            if len(member_count) == 3:
                coordinates[0] = [self.width / 3 - 67, 3]
                coordinates[1] = [self.width / 3 - 70, 0]

        if team == "vegetables":
            if len(member_count) == 1:
                coordinates[0] = [self.width / 2 + 64, 3]
                coordinates[1] = [self.width / 2 + 60, 0]

            if len(member_count) == 2:
                coordinates[0] = [self.width / 2 + 64, 3]
                coordinates[1] = [self.width / 2 + 60, 0]

            if len(member_count) == 3:
                coordinates[0] = [self.width / 2 + 58, 3]
                coordinates[1] = [self.width / 2 + 54, 0]

        return coordinates


def setup(bot: Bot) -> None:
    """Add the cog to the bot."""
    bot.add_cog(TeamCount(bot))
