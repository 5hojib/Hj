from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import pyrogram
from pyrogram import raw, types

if TYPE_CHECKING:
    from collections.abc import Iterable

log = logging.getLogger(__name__)


class GetStories:
    async def get_stories(
        self: pyrogram.Client,
        chat_id: int | str,
        story_ids: int | Iterable[int],
    ) -> types.Story | list[types.Story]:
        """Get one or more story from an user by using story identifiers.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target user/channel.
                For your personal story you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).
                You can also use user profile/channel public link in form of *t.me/<username>* (str).

            story_ids (``int`` | Iterable of ``int``):
                Pass a single story identifier or an iterable of story ids (as integers) to get the content of the
                story themselves.

        Returns:
            :obj:`~pyrogram.types.Story` | List of :obj:`~pyrogram.types.Story`: In case *story_ids* was not
            a list, a single story is returned, otherwise a list of stories is returned.

        Example:
            .. code-block:: python

                # Get one story
                await app.get_stories(chat_id, 12345)

                # Get more than one story (list of stories)
                await app.get_stories(chat_id, [12345, 12346])

        Raises:
            ValueError: In case of invalid arguments.
        """

        peer = await self.resolve_peer(chat_id)

        is_iterable = not isinstance(story_ids, int)
        ids = list(story_ids) if is_iterable else [story_ids]

        rpc = raw.functions.stories.GetStoriesByID(peer=peer, id=ids)

        r = await self.invoke(rpc, sleep_threshold=-1)

        if is_iterable:
            return types.List(
                [await types.Story._parse(self, story, peer) for story in r.stories],
            )
        return (
            await types.Story._parse(self, r.stories[0], peer)
            if r.stories and len(r.stories) > 0
            else None
        )
