from __future__ import annotations

import logging

import pyrogram
from pyrogram import raw

log = logging.getLogger(__name__)


class GetChatHistoryCount:
    async def get_chat_history_count(
        self: pyrogram.Client,
        chat_id: int | str,
    ) -> int:
        """Get the total count of messages in a chat.

        .. note::

            Due to Telegram latest internal changes, the server can't reliably find anymore the total count of messages
            a **private** or a **basic group** chat has with a single method call. To overcome this limitation, Pyrogram
            has to iterate over all the messages. Channels and supergroups are not affected by this limitation.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                You can also use chat public link in form of *t.me/<username>* (str).

        Returns:
            ``int``: On success, the chat history count is returned.

        Example:
            .. code-block:: python

                await app.get_history_count(chat_id)
        """

        r = await self.invoke(
            raw.functions.messages.GetHistory(
                peer=await self.resolve_peer(chat_id),
                offset_id=0,
                offset_date=0,
                add_offset=0,
                limit=1,
                max_id=0,
                min_id=0,
                hash=0,
            ),
        )

        if isinstance(r, raw.types.messages.Messages):
            return len(r.messages)
        return r.count
