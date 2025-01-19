from __future__ import annotations

import pyrogram
from pyrogram import enums, raw


class SearchGlobalCount:
    async def search_global_count(
        self: pyrogram.Client,
        query: str = "",
        filter: enums.MessagesFilter = enums.MessagesFilter.EMPTY,
    ) -> int:
        """Get the count of messages resulting from a global search.

        If you want to get the actual messages, see :meth:`~pyrogram.Client.search_global`.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            query (``str``, *optional*):
                Text query string.
                Use "@" to search for mentions.

            filter (:obj:`~pyrogram.enums.MessagesFilter`, *optional*):
                Pass a filter in order to search for specific kind of messages only:

        Returns:
            ``int``: On success, the messages count is returned.
        """
        r = await self.invoke(
            raw.functions.messages.SearchGlobal(
                q=query,
                filter=filter.value(),
                min_date=0,
                max_date=0,
                offset_rate=0,
                offset_peer=raw.types.InputPeerEmpty(),
                offset_id=0,
                limit=1,
            ),
        )

        if hasattr(r, "count"):
            return r.count
        return len(r.messages)
