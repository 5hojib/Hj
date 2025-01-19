from __future__ import annotations

from typing import TYPE_CHECKING

import pyrogram
from pyrogram import raw, types, utils
from pyrogram.file_id import (
    FileId,
    FileType,
    FileUniqueId,
    FileUniqueType,
)
from pyrogram.types.object import Object

if TYPE_CHECKING:
    from datetime import datetime


class AlternativeVideo(Object):
    """Describes an alternative reencoded quality of a video file.

    Parameters:
        file_id (``str``):
            Identifier for this file, which can be used to download or reuse the file.

        file_unique_id (``str``):
            Unique identifier for this file, which is supposed to be the same over time and for different accounts.
            Can't be used to download or reuse the file.

        width (``int``):
            Video width as defined by sender.

        height (``int``):
            Video height as defined by sender.

        codec (``str``):
            Codec used for video file encoding, for example, "h264", "h265", or "av1".

        duration (``int``):
            Duration of the video in seconds as defined by sender.

        file_name (``str``, *optional*):
            Video file name.

        mime_type (``str``, *optional*):
            Mime type of a file as defined by sender.

        file_size (``int``, *optional*):
            File size.

        supports_streaming (``bool``, *optional*):
            True, if the video was uploaded with streaming support.

        date (:py:obj:`~datetime.datetime`, *optional*):
            Date the video was sent.

        thumbs (List of :obj:`~pyrogram.types.Thumbnail`, *optional*):
            Video thumbnails.

    """

    def __init__(
        self,
        *,
        client: pyrogram.Client = None,
        file_id: str,
        file_unique_id: str,
        width: int,
        height: int,
        codec: str,
        duration: int,
        file_name: str | None = None,
        mime_type: str | None = None,
        file_size: int | None = None,
        supports_streaming: bool | None = None,
        date: datetime | None = None,
        thumbs: list[types.Thumbnail] | None = None,
    ) -> None:
        super().__init__(client)
        self.file_id = file_id
        self.file_unique_id = file_unique_id
        self.width = width
        self.height = height
        self.codec = codec
        self.duration = duration
        self.file_name = file_name
        self.mime_type = mime_type
        self.file_size = file_size
        self.supports_streaming = supports_streaming
        self.date = date
        self.thumbs = thumbs

    @staticmethod
    def _parse(
        client: pyrogram.Client,
        video: raw.types.Document,
        video_attributes: raw.types.DocumentAttributeVideo,
        file_name: str,
    ) -> AlternativeVideo:
        file_id = (
            FileId(
                file_type=FileType.VIDEO,
                dc_id=video.dc_id,
                media_id=video.id,
                access_hash=video.access_hash,
                file_reference=video.file_reference,
            ).encode()
            if video
            else None
        )

        file_unique_id = (
            FileUniqueId(
                file_unique_type=FileUniqueType.DOCUMENT,
                media_id=video.id,
            ).encode()
            if video
            else None
        )

        return AlternativeVideo(
            client=client,
            file_id=file_id,
            file_unique_id=file_unique_id,
            width=video_attributes.w if video_attributes else 0,
            height=video_attributes.h if video_attributes else 0,
            codec=video_attributes.video_codec if video_attributes else "",
            duration=video_attributes.duration if video_attributes else 0,
            file_name=file_name,
            mime_type=video.mime_type if video else "",
            supports_streaming=video_attributes.supports_streaming
            if video_attributes
            else False,
            file_size=video.size if video else 0,
            date=utils.timestamp_to_datetime(video.date) if video else None,
            thumbs=types.Thumbnail._parse(client, video) if video else None,
        )
