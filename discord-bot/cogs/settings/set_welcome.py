"""Setting util for join and leave features"""

import discord
from discord.ext import commands
from typing import Optional

from utils import settings
from utils.output import done, not_done
from utils.parsers import parse_message_url


class SetWelcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def cog_check(self, ctx):
        """This cog is for server admins only"""
        return ctx.author.guild_permissions.administrator

    @commands.command(
        name="setwelcomechannel", 
        aliases=["swc"],
        help="Sets up the channel where welcome messages will be sent.",
    )
    async def setwelcomechannel(
        self, 
        ctx, 
        channel:Optional[discord.TextChannel]=None
    ):
        res = await settings.set_guild_param(
            self.bot, 
            user_id=ctx.author.id,
            guild_id=ctx.guild.id,
            welcome_channel_id=channel.id if channel else None
        )
        if res.status != 200:
            return await not_done(ctx, await res.text())
        await done(ctx)

    @commands.command(
        name="setinitialwelcomemessage", 
        aliases=["siwm"],
        help="Sets up the initial welcome message to the contents of the message, link to which you provide.",
    )
    async def setinitialwelcomemessage(
        self, 
        ctx, 
        link:str=None
    ):
        _, _, message = parse_message_url(link, self.bot)
        res = await settings.set_guild_param(
            self.bot, 
            user_id=ctx.author.id,
            guild_id=ctx.guild.id,
            welcome_initial_message_text=message.content,
            welcome_initial_message_embed=message.embed.to_dict(),
        )
        if res.status != 200:
            return await not_done(ctx, await res.text())
        await done(ctx)

    @commands.command(
        name="setacceptwelcomemessage", 
        aliases=["sawm"],
        help="Sets up the welcome message that would be sent when a new user accepts the server rules to the contents of the message, link to which you provide.",
    )
    async def setinitialwelcomemessage(
        self, 
        ctx, 
        link:str=None
    ):
        _, _, message = parse_message_url(link, self.bot)
        res = await settings.set_guild_param(
            self.bot, 
            user_id=ctx.author.id,
            guild_id=ctx.guild.id,
            welcome_accept_message_text=message.content,
            welcome_accept_message_embed=message.embed.to_dict(),
        )
        if res.status != 200:
            return await not_done(ctx, await res.text())
        await done(ctx)

    @commands.command(
        name="setaleavemessage", 
        aliases=["slm"],
        help="Sets up the leave message that would be sent when a user leaves the server to the contents of the message, link to which you provide.",
    )
    async def setaleavemessage(
        self, 
        ctx, 
        link:str=None
    ):
        _, _, message = parse_message_url(link, self.bot)
        res = await settings.set_guild_param(
            self.bot, 
            user_id=ctx.author.id,
            guild_id=ctx.guild.id,
            leave_message_text=message.content,
            leave_message_embed=message.embed.to_dict(),
        )
        if res.status != 200:
            return await not_done(ctx, await res.text())
        await done(ctx)

def setup(bot):
    bot.add_cog(SetWelcome(bot))