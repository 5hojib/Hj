from __future__ import annotations

import pyrogram
from pyrogram import raw, types, utils
from pyrogram.types.object import Object


class StoryForwardHeader(Object):
    """Contains information about origin of forwarded story.


    Parameters:
        user (:obj:`~pyrogram.types.User`, *optional*):
            Sender of the story.

        sender_name (``str``, *optional*):
            For stories forwarded from users who have hidden their accounts, name of the user.

        chat (:obj:`~pyrogram.types.Chat`, *optional*):
            Sender of the story. If the story is from channel.

        story_id (``int``):
            Unique identifier for the original story.

        is_modified (``bool``):
            True, if the story is modified.
    """

    def __init__(
        self,
        *,
        user: types.User = None,
        sender_name: str | None = None,
        chat: types.Chat = None,
        story_id: int | None = None,
        is_modified: bool | None = None,
    ) -> None:
        super().__init__()

        self.user = user
        self.sender_name = sender_name
        self.chat = chat
        self.story_id = story_id
        self.is_modified = is_modified

    async def _parse(
        self: pyrogram.Client,
        fwd_header: raw.types.StoryFwdHeader,
    ) -> StoryForwardHeader:
        user = None
        chat = None
        if fwd_header.from_peer is not None:
            if isinstance(fwd_header.from_peer, raw.types.PeerChannel):
                chat = await self.get_chat(
                    utils.get_channel_id(fwd_header.from_peer.channel_id),
                )
            elif isinstance(fwd_header.from_peer, raw.types.InputPeerSelf):
                user = self.me
            else:
                user = await self.get_users(fwd_header.from_peer.user_id)

        return StoryForwardHeader(
            user=user,
            sender_name=fwd_header.from_name,
            chat=chat,
            story_id=fwd_header.story_id,
            is_modified=fwd_header.modified,
        )
