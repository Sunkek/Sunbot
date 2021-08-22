"""Helper functions to address the settings REST API"""

import os

HOST = (
    f"http://{os.environ.get('DISCORD_SETTINGS_HOST', 'localhost')}:"
    f"{os.environ.get('DISCORD_SETTINGS_PORT', '8000')}"
)
URLS = {
    "guild_settings":f"{HOST}/discord/guild/set/",
    "guild_resettings":f"{HOST}/discord/guild/reset/",
    "user_settings":f"{HOST}/discord/user/set/",
}

async def set_guild_param(bot, user_id, guild_id, **kwargs):
    """Change guild settings"""
    return await bot.web_client.post(
        f"{URLS['guild_settings']}{guild_id}", 
        headers={"Invoker": str(user_id)},
        json=kwargs
    )
    
async def set_user_param(bot, user_id, **kwargs):
    """Change user settings"""
    return await bot.web_client.post(
        f"{URLS['user_settings']}{user_id}/", 
        json=kwargs
    )