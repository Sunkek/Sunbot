"""Miscellaneous commands"""

from discord.ext import commands

from utils import output


class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="ping",
        brief="Good for testing if the bot works",
    )
    async def ping(self, ctx):
        await output.respond(ctx, t="Pong!")


def setup(bot):
    bot.add_cog(Misc(bot))