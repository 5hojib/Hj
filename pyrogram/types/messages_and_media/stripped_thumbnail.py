from __future__ import annotations

from typing import TYPE_CHECKING

from pyrogram.types.object import Object

if TYPE_CHECKING:
    import pyrogram
    from pyrogram import raw


class StrippedThumbnail(Object):
    """A stripped thumbnail

    Parameters:
        data (``bytes``):
            Thumbnail data
    """

    def __init__(self, *, client: pyrogram.Client = None, data: bytes) -> None:
        super().__init__(client)

        self.data = data

    @staticmethod
    def _parse(
        client,
        stripped_thumbnail: raw.types.PhotoStrippedSize,
    ) -> StrippedThumbnail:
        return StrippedThumbnail(data=stripped_thumbnail.bytes, client=client)
