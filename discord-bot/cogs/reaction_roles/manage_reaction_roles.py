"""Reaction roles creation and editing"""

import typing
import re
from asyncio import TimeoutError

from discord import Color, Embed, TextChannel
from discord.ext import commands

from utils import output, reaction_roles, parsers

NEW_RR_EMBED = Embed(
    title="Reaction roles",
    description="Click on the reactions below to get the roles",
)

class ReactionRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(
        name="reactionroles", 
        aliases=["rr"],
        help="Command group for managing reaction roles",
        invoke_without_command=True
    )
    async def manage_reaction_roles(self, ctx):
        await respond(ctx, "Reaction roles root!") # TODO return help
        
    @manage_reaction_roles.command(
        name="add", 
        aliases=["a"],
        help="Creates new reaction roles message. You can specify a channel to send a new message or provide a message link. The bot will edit its own reaction roles message with the roles it assigns.", 
    )
    async def add_reaction_roles(
        self, ctx, message_url: typing.Union[TextChannel, str]=None
    ):
        if message_url is None:  # Defaults to current channel
            message_url = ctx.channel
        if isinstance(message_url, TextChannel):  # New embed if channel provided
            message = await message_url.send(embed=NEW_RR_EMBED)
        else:
            guild, channel, message = await parsers.parse_message_url(
                message_url, self.bot
            )
            if guild != ctx.guild:
                raise ValueError("Must be a message from this server")
        res = await reaction_roles.new_reaction_roles_message(
            self.bot, ctx.author.id, ctx.guild.id, ctx.channel.id, message.id
        )
        print(await res.json()) # TODO work with res

        await output.respond(
            ctx,
            t="Add reaction roles", 
            d="Send an emote and ping the role you want to add, like `emote @role` or `emote role_id`. Send `done` when done", 
            c=Color.gold()
        )

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        done = False
        while not done:
            try:
                rr_pair_message = await self.bot.wait_for(
                    "message", timeout=30.0, check=check
                )
                if rr_pair_message.content.lower() == "done":
                    break
                emote, role = await parsers.parse_reaction_role_pair(
                    rr_pair_message.content, ctx
                )                
                res = await reaction_roles.add_reaction_role(
                    self.bot, ctx.author.id, emote, role.id, message.id,
                )
                print(await res.json()) # TODO work with res

                if message.author == ctx.guild.me:
                    new_embed = message.embeds[0] if message.embeds else NEW_RR_EMBED
                    roles_field = -1
                    for num, field in enumerate(new_embed.fields):
                        if field.name.lower() == "roles":
                            roles_field = num
                            value = field.value + f"\n{emote} {role.mention}"
                            new_embed.set_field_at(roles_field, name="Roles", value=value)
                    if roles_field == -1:
                        new_embed.add_field(name="Roles", value=f"{emote} {role.mention}")
                    await message.edit(embed=new_embed)

                await message.add_reaction(emote)
                await output.ok(rr_pair_message)

            except TimeoutError:
                done = True
            except ValueError as e:
                await output.not_done(rr_pair_message, e)


        await output.done(ctx)

def setup(bot):
    bot.add_cog(ReactionRoles(bot))
