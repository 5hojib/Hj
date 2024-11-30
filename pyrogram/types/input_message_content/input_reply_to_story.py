from __future__ import annotations

from pyrogram import raw
from pyrogram.types.object import Object


class InputReplyToStory(Object):
    """Contains information about a target replied story.


    Parameters:
        peer (:obj:`~pyrogram.raw.types.InputPeer`):
            An InputPeer.

        story_id (``int``):
            If the message is a reply, ID of the target story.
    """

    def __init__(
        self,
        *,
        peer: raw.types.InputPeer = None,
        story_id: int | None = None,
    ) -> None:
        super().__init__()

        self.peer = peer
        self.story_id = story_id

    def write(self):
        return raw.types.InputReplyToStory(
            peer=self.peer,
            story_id=self.story_id,
        ).write()
