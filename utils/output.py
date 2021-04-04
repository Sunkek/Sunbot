import discord

MT = discord.Embed.Empty

async def respond(ctx, txt=None, t=MT, d=MT, c=None):
    """Send a response with provided text. Return the message object"""
    c = c or ctx.author.color
    if t or d:
        e = discord.Embed(title=t, description=d)
        if c: e.color = c
        return await ctx.reply(txt, embed=e, mention_author=False)
    return await ctx.reply(txt, mention_author=False)