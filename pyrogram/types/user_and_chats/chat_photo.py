from __future__ import annotations

import pyrogram
from pyrogram import raw, types
from pyrogram.file_id import (
    FileId,
    FileType,
    FileUniqueId,
    FileUniqueType,
    ThumbnailSource,
)
from pyrogram.types.object import Object


class ChatPhoto(Object):
    """A chat photo.

    Parameters:
        small_file_id (``str``):
            File identifier of small (160x160) chat photo.
            This file_id can be used only for photo download and only for as long as the photo is not changed.

        small_photo_unique_id (``str``):
            Unique file identifier of small (160x160) chat photo, which is supposed to be the same over time and for
            different accounts. Can't be used to download or reuse the file.

        big_file_id (``str``):
            File identifier of big (640x640) chat photo.
            This file_id can be used only for photo download and only for as long as the photo is not changed.

        big_photo_unique_id (``str``):
            Unique file identifier of big (640x640) chat photo, which is supposed to be the same over time and for
            different accounts. Can't be used to download or reuse the file.

        has_animation (``bool``):
            True, if the photo has animated variant

        is_personal (``bool``):
            True, if the photo is visible only for the current user

        minithumbnail (:obj:`~pyrogram.types.StrippedThumbnail`, *optional*):
            User profile photo minithumbnail; may be None.

    """

    def __init__(
        self,
        *,
        client: pyrogram.Client = None,
        small_file_id: str,
        small_photo_unique_id: str,
        big_file_id: str,
        big_photo_unique_id: str,
        has_animation: bool,
        is_personal: bool,
        minithumbnail: types.StrippedThumbnail = None,
    ) -> None:
        super().__init__(client)

        self.small_file_id = small_file_id
        self.small_photo_unique_id = small_photo_unique_id
        self.big_file_id = big_file_id
        self.big_photo_unique_id = big_photo_unique_id
        self.has_animation = has_animation
        self.is_personal = is_personal
        self.minithumbnail = minithumbnail

    @staticmethod
    def _parse(
        client,
        chat_photo: raw.types.UserProfilePhoto | raw.types.ChatPhoto,
        peer_id: int,
        peer_access_hash: int,
    ):
        if not isinstance(
            chat_photo,
            raw.types.UserProfilePhoto | raw.types.ChatPhoto,
        ):
            return None

        return ChatPhoto(
            small_file_id=FileId(
                file_type=FileType.CHAT_PHOTO,
                dc_id=chat_photo.dc_id,
                media_id=chat_photo.photo_id,
                access_hash=0,
                volume_id=0,
                thumbnail_source=ThumbnailSource.CHAT_PHOTO_SMALL,
                local_id=0,
                chat_id=peer_id,
                chat_access_hash=peer_access_hash,
            ).encode(),
            small_photo_unique_id=FileUniqueId(
                file_unique_type=FileUniqueType.DOCUMENT,
                media_id=chat_photo.photo_id,
            ).encode(),
            big_file_id=FileId(
                file_type=FileType.CHAT_PHOTO,
                dc_id=chat_photo.dc_id,
                media_id=chat_photo.photo_id,
                access_hash=0,
                volume_id=0,
                thumbnail_source=ThumbnailSource.CHAT_PHOTO_BIG,
                local_id=0,
                chat_id=peer_id,
                chat_access_hash=peer_access_hash,
            ).encode(),
            big_photo_unique_id=FileUniqueId(
                file_unique_type=FileUniqueType.DOCUMENT,
                media_id=chat_photo.photo_id,
            ).encode(),
            has_animation=chat_photo.has_video,
            is_personal=getattr(chat_photo, "personal", False),
            minithumbnail=types.StrippedThumbnail(data=chat_photo.stripped_thumb)
            if chat_photo.stripped_thumb
            else None,
            client=client,
        )
