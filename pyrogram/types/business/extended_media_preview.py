from __future__ import annotations

from pyrogram import raw, types
from pyrogram.types.object import Object


class ExtendedMediaPreview(Object):
    """A ExtendedMediaPreview.

    Parameters:
        width (``int``, *optional*):
            Media Width.

        height (``int``, *optional*):
            Media Height.

        thumb (:obj:`~pyrogram.types.StrippedThumbnail`, *optional*):
            Media Thumbnail.

        video_duration (``int``, *optional*):
            Video duration.
    """

    def __init__(
        self,
        *,
        width: int | None = None,
        height: int | None = None,
        thumb: types.Thumbnail = None,
        video_duration: int | None = None,
    ) -> None:
        super().__init__()

        self.width = width
        self.height = height
        self.thumb = thumb
        self.video_duration = video_duration

    @staticmethod
    def _parse(
        client,
        media: raw.types.MessageExtendedMediaPreview,
    ) -> ExtendedMediaPreview:
        thumb = None
        if media.thumb:
            thumb = types.StrippedThumbnail._parse(client, media.thumb)

        return ExtendedMediaPreview(
            width=media.w,
            height=media.h,
            thumb=thumb,
            video_duration=media.video_duration,
        )
