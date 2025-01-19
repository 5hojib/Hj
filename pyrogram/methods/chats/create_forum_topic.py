from __future__ import annotations

import pyrogram
from pyrogram import raw, types


class CreateForumTopic:
    async def create_forum_topic(
        self: pyrogram.Client,
        chat_id: int | str,
        title: str,
        icon_color: int | None = None,
        icon_emoji_id: int | None = None,
    ) -> types.ForumTopicCreated:
        """Create a new forum topic.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                You can also use chat public link in form of *t.me/<username>* (str).

            title (``str``):
                The forum topic title.

            icon_color (``int``, *optional*):
                The color of forum topic icon.

            icon_emoji_id (``int``, *optional*):
                Unique identifier of the custom emoji shown as the topic icon

        Returns:
            :obj:`~pyrogram.types.ForumTopicCreated`: On success, a forum_topic_created object is returned.

        Example:
            .. code-block:: python

                await app.create_forum_topic("Topic Title")
        """
        r = await self.invoke(
            raw.functions.channels.CreateForumTopic(
                channel=await self.resolve_peer(chat_id),
                title=title,
                random_id=self.rnd_id(),
                icon_color=icon_color,
                icon_emoji_id=icon_emoji_id,
            ),
        )

        return types.ForumTopicCreated._parse(r.updates[1].message)
