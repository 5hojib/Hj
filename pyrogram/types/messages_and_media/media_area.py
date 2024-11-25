from __future__ import annotations

import pyrogram
from pyrogram import raw, types
from pyrogram.types.object import Object


class MediaArea(Object):
    """Content of a media areas in story.

    It should be one of:

    - :obj:`~pyrogram.types.MediaAreaChannelPost`
    """

    def __init__(self, coordinates: types.MediaAreaCoordinates) -> None:
        super().__init__()

        self.coordinates = coordinates

    async def _parse(
        self: pyrogram.Client,
        media_area: raw.base.MediaArea,
    ) -> MediaArea:
        if isinstance(media_area, raw.types.MediaAreaChannelPost):
            return await types.MediaAreaChannelPost._parse(self, media_area)
        return None
