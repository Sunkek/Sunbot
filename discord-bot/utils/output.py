from typing import Union
from random import choice, seed

from discord import Embed, Color, Message
from discord.ext.commands import Context

MT = Embed.Empty
OK_TITLES = (
    "Done", "Success", "OK", "It worked", "There you go", "There, you happy?",
    "Alright", "Completed", "No errors", "Anything else?"
)
ERROR_TITLES = (
    "No", "Nope", "I don't think so", "Not gonna happen", "Nah", "Not likely", 
    "Fat chance", "Fuck you", "Good try, asshole", "No way", 
    "Did you really think I would do that?", "Do this shit yourself",
    "I am not your bitch", "You didn't ask nice enough", "Not doing that"
)  

async def respond(ctx, txt=None, t=MT, d=MT, c=None):
    """Send a response with provided text. Return the message object"""
    c = c or ctx.author.color
    if t != MT or d != MT:
        e = Embed(title=t, description=d)
        if c: e.color = c
        return await ctx.reply(txt, embed=e, mention_author=False)
    return await ctx.reply(txt, mention_author=False)

async def done(ctx):
    seed()
    await respond(
        ctx, 
        t=choice(OK_TITLES),
        c=Color(0x80ff80),
    )

async def not_done(ctx, error=None):
    seed()
    await respond(
        ctx, 
        t=choice(ERROR_TITLES),
        d=str(error) if error else MT,
        c=Color(0xff7f7f),
    )

async def ok(msg: Union[Context, Message]):
    if isinstance(ctx, Context):
        msg = ctx.message
    await msg.add_reaction("👌")
    
async def not_ok(ctx):
    await ctx.message.add_reaction("✋")