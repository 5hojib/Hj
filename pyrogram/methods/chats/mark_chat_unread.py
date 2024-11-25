from __future__ import annotations

import pyrogram
from pyrogram import raw


class MarkChatUnread:
    async def mark_chat_unread(
        self: pyrogram.Client,
        chat_id: int | str,
    ) -> bool:
        """Mark a chat as unread.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                You can also use chat public link in form of *t.me/<username>* (str).

        Returns:
            ``bool``: On success, True is returned.
        """

        return await self.invoke(
            raw.functions.messages.MarkDialogUnread(
                peer=await self.resolve_peer(chat_id),
                unread=True,
            ),
        )
