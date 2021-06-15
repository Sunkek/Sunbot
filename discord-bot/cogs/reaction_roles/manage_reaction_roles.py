"""Reaction roles creation and editing"""

import typing
import re

import discord
from discord.ext import commands

from utils import output, reaction_roles

re_url_pattern = "([0-9]+)\/([0-9]+)\/([0-9]+)"


class ReactionRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.new_rr = discord.Embed(
            title="Reaction roles",
            description="Click on the reactions below to get the roles",
        )

    @commands.group(
        name="reactionroles", 
        aliases=["rr"],
        help="Command group for managing reaction roles",
        invoke_without_command=True
    )
    async def manage_reaction_roles(self, ctx):
        await respond(ctx, "Reaction roles root!") # TODO return help
        
    @manage_reaction_roles.command(
        name="new", 
        aliases=["n"],
        help="Creates new reaction roles message. You can specify a channel to send a new message or provide a message link. The bot will edit its own reaction roles message with the roles it assigns.", 
    )
    async def new_reaction_roles(self, ctx, message_url: typing.Union[discord.TextChannel, str]):
        print(message_url)
        if isinstance(message_url, discord.TextChannel):
            message_url = await message.send(embed=self.new_rr)
            message_url = message.jump_url
        else:
            m = re.search(re_url_pattern, message_url)
            if m is None:
                raise ValueError("Invalid message URL")
            guild = self.bot.get_guild(int(m.group(1)))
            channel = guild.get_guild(int(m.group(2)))
            message = await channel.fetch_message(int(m.group(3)))
            if message.author == ctx.guild.me:
                if not message.embeds:
                    await message.edit(embed=self.new_rr)       
        res = await reaction_roles.new_reaction_roles(
            self.bot, ctx.author.id, message_url
        )
        print(res.__dict__) # TODO work with res
        await ok(ctx)


def setup(bot):
    bot.add_cog(ReactionRoles(bot))