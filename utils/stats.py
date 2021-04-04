"""Helper functions to address the stats REST API"""

import os

HOST = (
    f"http://{os.environ.get('DISCORD_STATS_HOST', 'localhost')}:"
    f":{os.environ.get('DISCORD_STATS_PORT', '8000')}"
)
URLS = {
    "messages":f"{HOST}/api/v1/messages/",
}
        
async def add_message(bot, **kwargs):
    await bot.web.post(URLS["messages"], json=kwargs)
