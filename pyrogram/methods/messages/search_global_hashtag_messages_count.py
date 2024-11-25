from __future__ import annotations

import pyrogram
from pyrogram import raw


class SearchGlobalHashtagMessagesCount:
    async def search_global_hashtag_messages_count(
        self: pyrogram.Client,
        hashtag: str = "",
    ) -> int:
        """Get the count of messages with the provided hashtag.

        If you want to get the actual messages, see :meth:`~pyrogram.Client.search_public_hashtag_messages`.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            hashtag (``str``, *optional*):
                Hashtag to search for.

        Returns:
            ``int``: On success, the messages count is returned.

        """
        r = await self.invoke(
            raw.functions.channels.SearchPosts(
                hashtag=hashtag,
                offset_rate=0,
                offset_peer=raw.types.InputPeerEmpty(),
                offset_id=0,
                limit=1,
            ),
        )

        if hasattr(r, "count"):
            return r.count
        return len(r.messages)
