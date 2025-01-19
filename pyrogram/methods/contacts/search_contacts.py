from __future__ import annotations

import pyrogram
from pyrogram import raw, types


class SearchContacts:
    async def search_contacts(
        self: pyrogram.Client,
        query: str,
        limit: int = 0,
    ) -> types.FoundContacts:
        """Returns users or channels found by name substring and auxiliary data.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            query (``str``):
                Target substring.
            limit (``int``, *optional*):
                Maximum number of users to be returned.

        Returns:
            :obj:`~pyrogram.types.FoundContacts`: On success, a list of chats is returned.

        Example:
            .. code-block:: python

                await app.search_contacts("pyrogram")
        """
        total = limit or (1 << 31) - 1
        limit = min(100, total)

        r = await self.invoke(raw.functions.contacts.Search(q=query, limit=limit))

        return types.FoundContacts._parse(self, r)
