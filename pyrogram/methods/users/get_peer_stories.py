from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import pyrogram
from pyrogram import raw, types

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

log = logging.getLogger(__name__)


class GetPeerStories:
    async def get_peer_stories(
        self: pyrogram.Client,
        chat_id: int | str,
    ) -> AsyncGenerator[types.Story, None] | None:
        """Get all active stories from an user/channel by using user identifiers.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target user/channel.
                For your personal story you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).
                You can also use user profile/channel public link in form of *t.me/<username>* (str).

        Returns:
            ``Generator``: On success, a generator yielding :obj:`~pyrogram.types.Story` objects is returned.

        Example:
            .. code-block:: python

                # Get all active story from spesific user/channel
                async for story in app.get_peer_stories(chat_id):
                    print(story)

        Raises:
            ValueError: In case of invalid arguments.
        """

        peer = await self.resolve_peer(chat_id)

        rpc = raw.functions.stories.GetPeerStories(peer=peer)

        r = await self.invoke(rpc, sleep_threshold=-1)

        for story in r.stories.stories:
            yield await types.Story._parse(self, story, peer)
