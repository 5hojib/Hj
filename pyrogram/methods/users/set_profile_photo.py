from __future__ import annotations

from typing import BinaryIO

import pyrogram
from pyrogram import raw


class SetProfilePhoto:
    async def set_profile_photo(
        self: pyrogram.Client,
        *,
        photo: str | BinaryIO | None = None,
        video: str | BinaryIO | None = None,
    ) -> bool:
        """Set a new profile photo or video (H.264/MPEG-4 AVC video, max 5 seconds).

        The ``photo`` and ``video`` arguments are mutually exclusive.
        Pass either one as named argument (see examples below).

        .. note::

            This method only works for Users.
            Bots profile photos must be set using BotFather.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            photo (``str`` | ``BinaryIO``, *optional*):
                Profile photo to set.
                Pass a file path as string to upload a new photo that exists on your local machine or
                pass a binary file-like object with its attribute ".name" set for in-memory uploads.

            video (``str`` | ``BinaryIO``, *optional*):
                Profile video to set.
                Pass a file path as string to upload a new video that exists on your local machine or
                pass a binary file-like object with its attribute ".name" set for in-memory uploads.

        Returns:
            ``bool``: True on success.

        Example:
            .. code-block:: python

                # Set a new profile photo
                await app.set_profile_photo(photo="new_photo.jpg")

                # Set a new profile video
                await app.set_profile_photo(video="new_video.mp4")
        """

        return bool(
            await self.invoke(
                raw.functions.photos.UploadProfilePhoto(
                    file=await self.save_file(photo),
                    video=await self.save_file(video),
                ),
            ),
        )
