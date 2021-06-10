"""Helper functions to address the settings REST API"""

import os

HOST = (
    f"http://{os.environ.get('DISCORD_SETTINGS_HOST', 'localhost')}:"
    f":{os.environ.get('DISCORD_SETTINGS_PORT', '8000')}"
)
URLS = {
    "guild_settings":f"{HOST}/api/v1/settings/guild/",
    "user_settings":f"{HOST}/api/v1/settings/user/",
}

async def set_guild_param(bot, user_id, guild_id, **kwargs):
    """Change guild settings"""
    return await bot.web_client.patch(
        f"{URLS['guild_settings']}{guild_id}/", 
        headers={"Invoker": user_id},
        json=kwargs
    )
    
async def set_user_param(bot, user_id, **kwargs):
    """Change user settings"""
    return await bot.web_client.patch(
        f"{URLS['user_settings']}{user_id}/", 
        json=kwargs
    )