"""My own Discord bot, made to automate the boring admin work
and to track server statistics. Some of its features only work on 
`A Piece of Cake` server."""

import discord 
from discord.ext import commands

import aiohttp
import socket
import os
from random import choice, seed
from datetime import datetime

from utils import output

cogs = []
for (dirpath, dirnames, filenames) in os.walk(f"{os.getcwd()}/cogs/"):
    if "__pycache__" not in dirpath:
        cogs += [
            os.path.join(dirpath, f).replace(
                f"{os.getcwd()}/", ""
            ).replace(".py", "").replace("/", ".") .replace("\\", ".") 
            for f in filenames if "pycache" not in f
        ]

bot = commands.Bot(
    command_prefix=commands.when_mentioned_or("sb ", "SB ", "Sb "), 
    сase_insensitive=True,
)
bot.remove_command("help")  # Remove the default help command because there will be a custom one
bot.web_client = None
        
@bot.event
async def on_ready():
    if not bot.web_client:
        bot.web_client = aiohttp.ClientSession(
            loop=bot.loop,
            connector=aiohttp.TCPConnector( 
                family=socket.AF_INET,  # https://github.com/aio-libs/aiohttp/issues/2522#issuecomment-354454800
                ssl=False, 
                ),
            )
    if not bot.cogs:
        print("Loading cogs")
        for cog in cogs:
            try:
                if cog not in bot.cogs.values():
                    bot.load_extension(cog)
            except Exception as e:
                print(f"Error on loading {cog}:\n{e}")
        print("Cogs loaded")
    await bot.change_presence(activity=discord.Game(name=("sb ")))
    print(f"{bot.user} online")
    print(datetime.now())

@bot.event 
async def on_message(message):  
    # Without this it will ignore all commands if on_message listener present
    if not message.author.bot:
        await bot.process_commands(message)

@bot.event 
async def on_command_error(ctx, error):
    """Command error handler"""
    print(error)
    await output.not_done(ctx, error)

@commands.check(commands.is_owner())
@bot.command(description=f"`reload <cog name>` - reloads the specified cog")
async def reload(ctx, *, ext):
    cog = f"cogs.{ext}"
    try:
        bot.unload_extension(cog)
    except commands.ExtensionNotLoaded:
        pass
    bot.load_extension(cog)

bot.run(os.environ.get("DISCORD_BOT_TOKEN"))