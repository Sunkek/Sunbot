import re

from emoji import UNICODE_EMOJI
from discord.ext.commands import RoleConverter

emote_re = r":([^:\s]*)(?:::[^:\s]*)*:"

def parse_switch_opt(text):
    if text is None:
        return
    elif str(text).lower() in ("true", "1", "on"):
        return True
    elif str(text).lower() in ("false", "0", "off"):
        return False
    raise ValueError("Can't parse argument. Expected None, True or False")

async def parse_reaction_role_pair(text, ctx):
    emote, role = text.split()
    if emote in UNICODE_EMOJI:
        emote = str(bytes(str(emote), "utf-8")[:4], "utf-8")[0]  # Stripping skintones and other modifiers
    else: 
        name = re.search(emote_re, emote)
        emote = re.sub(name.group(1), r"_", emote)  # Wiping emote name to make it compact
    role = await RoleConverter().convert(ctx, role)
    return emote, role