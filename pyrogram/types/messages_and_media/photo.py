from __future__ import annotations

from typing import TYPE_CHECKING

import pyrogram
from pyrogram import raw, types, utils
from pyrogram.file_id import (
    FileId,
    FileType,
    FileUniqueId,
    FileUniqueType,
    ThumbnailSource,
)
from pyrogram.types.object import Object

if TYPE_CHECKING:
    from datetime import datetime


class Photo(Object):
    """A Photo.

    Parameters:
        file_id (``str``):
            Identifier for this file, which can be used to download or reuse the file.

        file_unique_id (``str``):
            Unique identifier for this file, which is supposed to be the same over time and for different accounts.
            Can't be used to download or reuse the file.

        width (``int``):
            Photo width.

        height (``int``):
            Photo height.

        file_size (``int``):
            File size.

        date (:py:obj:`~datetime.datetime`):
            Date the photo was sent.

        ttl_seconds (``int``, *optional*):
            Time-to-live seconds, for secret photos.

        thumbs (List of :obj:`~pyrogram.types.Thumbnail`, *optional*):
            Available thumbnails of this photo.
    """

    def __init__(
        self,
        *,
        client: pyrogram.Client = None,
        file_id: str,
        file_unique_id: str,
        width: int,
        height: int,
        file_size: int,
        date: datetime,
        ttl_seconds: int | None = None,
        thumbs: list[types.Thumbnail] | None = None,
    ) -> None:
        super().__init__(client)

        self.file_id = file_id
        self.file_unique_id = file_unique_id
        self.width = width
        self.height = height
        self.file_size = file_size
        self.date = date
        self.ttl_seconds = ttl_seconds
        self.thumbs = thumbs

    @staticmethod
    def _parse(
        client,
        photo: raw.types.Photo,
        ttl_seconds: int | None = None,
    ) -> Photo:
        if isinstance(photo, raw.types.Photo):
            photos: list[raw.types.PhotoSize] = []

            for p in photo.sizes:
                if isinstance(p, raw.types.PhotoSize):
                    photos.append(p)

                if isinstance(p, raw.types.PhotoSizeProgressive):
                    photos.append(
                        raw.types.PhotoSize(
                            type=p.type,
                            w=p.w,
                            h=p.h,
                            size=max(p.sizes),
                        ),
                    )

            photos.sort(key=lambda p: p.size)

            main = photos[-1]

            return Photo(
                file_id=FileId(
                    file_type=FileType.PHOTO,
                    dc_id=photo.dc_id,
                    media_id=photo.id,
                    access_hash=photo.access_hash,
                    file_reference=photo.file_reference,
                    thumbnail_source=ThumbnailSource.THUMBNAIL,
                    thumbnail_file_type=FileType.PHOTO,
                    thumbnail_size=main.type,
                    volume_id=0,
                    local_id=0,
                ).encode(),
                file_unique_id=FileUniqueId(
                    file_unique_type=FileUniqueType.DOCUMENT,
                    media_id=photo.id,
                ).encode(),
                width=main.w,
                height=main.h,
                file_size=main.size,
                date=utils.timestamp_to_datetime(photo.date),
                ttl_seconds=ttl_seconds,
                thumbs=types.Thumbnail._parse(client, photo),
                client=client,
            )
        return None
