from __future__ import annotations

import pyrogram
from pyrogram import raw


class GetChatOnlineCount:
    async def get_chat_online_count(
        self: pyrogram.Client,
        chat_id: int | str,
    ) -> int:
        """Get the number of members that are currently online in a chat.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                You can also use chat public link in form of *t.me/<username>* (str).

        Returns:
            ``int``: On success, the chat members online count is returned.

        Example:
            .. code-block:: python

                online = await app.get_chat_online_count(chat_id)
                print(online)
        """
        return (
            await self.invoke(
                raw.functions.messages.GetOnlines(
                    peer=await self.resolve_peer(chat_id),
                ),
            )
        ).onlines
