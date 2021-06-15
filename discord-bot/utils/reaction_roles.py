"""Helper functions to address the reaction roles REST API"""

import os

HOST = (
    f"http://{os.environ.get('REACTION_ROLES_HOST', 'localhost')}:"
    f":{os.environ.get('REACTION_ROLES_PORT', '8000')}"
)
URLS = {
    "reaction_roles_message":f"{HOST}/api/v1/reaction_roles/",
}

async def new_reaction_roles(bot, user_id, message_link):
    """Create new reaction roles message"""
    return await bot.web_client.post(
        f"{URLS['reaction_roles_message']}", 
        headers={"Invoker": user_id},
        json={"message_link": message_link},
    )
    