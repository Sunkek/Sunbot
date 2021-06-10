"""Setting cog for trackers"""

from discord.ext import commands
from typing import Optional

from utils import settings, parsers
from utils.output import respond, ok


class SetTrackers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(
        name="track", 
        aliases=["tr"],
        help="Command group for tracking your data",
    )
    async def set_track(self, ctx):
        await respond(ctx, "Command group root!")

    @set_track.command(
        name="messages", 
        aliases=["m"],
        help="Switches your message tracking setting on or off", 
    )
    async def set_track_messages(self, ctx, opt=None):
        opt = parsers.parse_switch_opt(opt)
        res = await settings.set_user_param(
            self.bot, ctx.author.id, track_messages=opt,
        )
        print(res.__dict__) # TODO work with res
        await ok(ctx)

def setup(bot):
    bot.add_cog(SetTrackers(bot))