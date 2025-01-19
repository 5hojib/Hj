from __future__ import annotations

import pyrogram
from pyrogram import raw


class CloseForumTopic:
    async def close_forum_topic(
        self: pyrogram.Client,
        chat_id: int | str,
        topic_id: int,
    ) -> bool:
        """Close a forum topic.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                You can also use chat public link in form of *t.me/<username>* (str).

            topic_id (``int``):
                Unique identifier (int) of the target forum topic.

        Returns:
            `bool`: On success, a Boolean is returned.

        Example:
            .. code-block:: python

                await app.close_forum_topic(chat_id, topic_id)
        """
        await self.invoke(
            raw.functions.channels.EditForumTopic(
                channel=await self.resolve_peer(chat_id),
                topic_id=topic_id,
                closed=True,
            ),
        )
        return True
