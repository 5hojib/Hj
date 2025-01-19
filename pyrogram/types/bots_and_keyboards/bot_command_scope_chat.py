from __future__ import annotations

import pyrogram
from pyrogram import raw

from .bot_command_scope import BotCommandScope


class BotCommandScopeChat(BotCommandScope):
    """Represents the scope of bot commands, covering a specific chat.

    Parameters:
        chat_id (``int`` | ``str``):
            Unique identifier for the target chat or username of the target supergroup (in the format
            @supergroupusername).
    """

    def __init__(self, chat_id: int | str) -> None:
        super().__init__("chat")

        self.chat_id = chat_id

    async def write(self, client: pyrogram.Client) -> raw.base.BotCommandScope:
        return raw.types.BotCommandScopePeer(
            peer=await client.resolve_peer(self.chat_id),
        )
