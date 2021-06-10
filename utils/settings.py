"""Helper functions to address the settings REST API"""

import os

HOST = (
    f"http://{os.environ.get('DISCORD_SETTINGS_HOST', 'localhost')}:"
    f":{os.environ.get('DISCORD_SETTINGS_PORT', '8000')}"
)
URLS = {
    "settings":f"{HOST}/api/v1/settings/",
}

async def set_guild_param(bot, guild_id, **kwargs):
    """Change guild settings"""
    return await bot.web_client.patch(f"{URLS['settings']}{guild_id}/", json=kwargs)