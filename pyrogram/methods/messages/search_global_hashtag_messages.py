from __future__ import annotations

from typing import TYPE_CHECKING

import pyrogram
from pyrogram import raw, types, utils

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator
    from datetime import datetime


class SearchGlobalHashtagMessages:
    async def search_global_hashtag_messages(
        self: pyrogram.Client,
        hashtag: str = "",
        offset_id: int = 0,
        offset_date: datetime | None = None,
        limit: int = 0,
    ) -> AsyncGenerator[types.Message, None]:
        """Searches for public channel posts with the given hashtag. For optimal performance, the number of returned messages is chosen by Telegram Server and can be smaller than the specified limit.

        If you want to get the posts count only, see :meth:`~pyrogram.Client.search_public_hashtag_messages_count`.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            hashtag (``str``, *optional*):
                Hashtag to search for.

            offset_id (``int``, *optional*):
                Offset of the first entry to return as received from the previous request; use empty string to get the first chunk of results.

            offset_date (:py:obj:`~datetime.datetime`, *optional*):
                Pass a date as offset to retrieve only older messages starting from that date.

            limit (``int``, *optional*):
                The maximum number of messages to be returned.
                By default, no limit is applied and all posts are returned.

        Returns:
            ``Generator``: A generator yielding :obj:`~pyrogram.types.Message` objects.

        Example:
            .. code-block:: python

                # Search for "#pyrogram". Get the first 50 results
                async for message in app.search_public_hashtag_messages("#pyrogram"):
                    print(message.text)

        """
        if offset_date is None:
            offset_date = utils.zero_datetime()
        current = 0
        total = abs(limit) or (1 << 31)
        limit = min(100, total)

        offset_peer = raw.types.InputPeerEmpty()

        while True:
            messages = await utils.parse_messages(
                self,
                await self.invoke(
                    raw.functions.channels.SearchPosts(
                        hashtag=hashtag,
                        offset_rate=utils.datetime_to_timestamp(offset_date),
                        offset_peer=offset_peer,
                        offset_id=offset_id,
                        limit=limit,
                    ),
                    sleep_threshold=60,
                ),
            )

            if not messages:
                return

            last = messages[-1]

            offset_date = utils.datetime_to_timestamp(last.date)
            offset_peer = await self.resolve_peer(last.chat.id)
            offset_id = last.id

            for message in messages:
                yield message

                current += 1

                if current >= total:
                    return
