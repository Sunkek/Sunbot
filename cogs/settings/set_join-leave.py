"""Setting util for uncategorizable things"""

import discord
from discord.ext import commands
from typing import Optional

from utils import settings


class SetGeneral(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def cog_check(self, ctx):
        """This cog is for server admins only"""
        return ctx.author.guild_permissions.administrator

    @commands.command(
        name="setwelcomechannel", 
        aliases=["swc"],
        description="Sets up the channel where welcome messages will be sent.",
    )
    async def setwelcomechannel(
        self, 
        ctx, 
        channel:Optional[discord.TextChannel]=None
    ):
        # Build and send the JSON to backend
        await settings.set_guild_param(
            self.bot, 
            guild_id=ctx.guild.id,
            welcome_channel_id=channel.id if channel else channel
        )         

def setup(bot):
    bot.add_cog(SetGeneral(bot))