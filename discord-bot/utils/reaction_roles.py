"""Helper functions to address the reaction roles REST API"""

import os

HOST = (
    f"http://{os.environ.get('REACTION_ROLES_HOST', 'localhost')}:"
    f"{os.environ.get('REACTION_ROLES_PORT', '8000')}"
)
URLS = {
    "reaction_roles_message":f"{HOST}/api/v1/message/",
    "reaction_roles_pair":f"{HOST}/api/v1/reaction_role/",
}

async def new_reaction_roles_message(bot, user_id, guild_id, channel_id, message_id):
    """Create new reaction roles message"""
    return await bot.web_client.post(
        f"{URLS['reaction_roles_message']}", 
        headers={"Invoker": str(user_id)},
        json={
            "guild_id": guild_id, 
            "channel_id": channel_id, 
            "message_id": message_id,
        },
    )

async def check_reaction_roles_message(bot, user_id, message_id):
    """Create new reaction roles message"""
    return await bot.web_client.get(
        f"{URLS['reaction_roles_message']}", 
        headers={"Invoker": str(user_id)},
        json={
            "message_id": message_id,
        },
    )

async def add_reaction_role(bot, user_id, emote, role_id, message_id):
    """Add a reaction role pair to the message"""
    return await bot.web_client.post(
        f"{URLS['reaction_roles_pair']}", 
        headers={"Invoker": str(user_id)},
        json={
            "emote": emote,
            "role_id": role_id,
            "message_id": message_id,
        },
    )
    