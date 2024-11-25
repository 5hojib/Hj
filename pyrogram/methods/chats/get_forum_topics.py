from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import pyrogram
from pyrogram import raw, types

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

log = logging.getLogger(__name__)


class GetForumTopics:
    async def get_forum_topics(
        self: pyrogram.Client,
        chat_id: int | str,
        limit: int = 0,
    ) -> AsyncGenerator[types.ForumTopic, None] | None:
        """Get one or more topic from a chat.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                You can also use chat public link in form of *t.me/<username>* (str).

            limit (``int``, *optional*):
                Limits the number of topics to be retrieved.

        Returns:
            ``Generator``: On success, a generator yielding :obj:`~pyrogram.types.ForumTopic` objects is returned.

        Example:
            .. code-block:: python

                # get all forum topics
                async for topic in app.get_forum_topics(chat_id):
                    print(topic)

        Raises:
            ValueError: In case of invalid arguments.
        """

        peer = await self.resolve_peer(chat_id)

        rpc = raw.functions.channels.GetForumTopics(
            channel=peer,
            offset_date=0,
            offset_id=0,
            offset_topic=0,
            limit=limit,
        )

        r = await self.invoke(rpc, sleep_threshold=-1)

        for _topic in r.topics:
            yield types.ForumTopic._parse(_topic)
