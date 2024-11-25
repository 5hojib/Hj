from __future__ import annotations

import math
from typing import BinaryIO

import pyrogram
from pyrogram import types
from pyrogram.file_id import FileId


class StreamMedia:
    async def stream_media(
        self: pyrogram.Client,
        message: types.Message | str,
        limit: int = 0,
        offset: int = 0,
    ) -> str | BinaryIO | None:
        """Stream the media from a message chunk by chunk.

        You can use this method to partially download a file into memory or to selectively download chunks of file.
        The chunk maximum size is 1 MiB (1024 * 1024 bytes).

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            message (:obj:`~pyrogram.types.Message` | ``str``):
                Pass a Message containing the media, the media itself (message.audio, message.video, ...) or a file id
                as string.

            limit (``int``, *optional*):
                Limit the amount of chunks to stream.
                Defaults to 0 (stream the whole media).

            offset (``int``, *optional*):
                How many chunks to skip before starting to stream.
                Defaults to 0 (start from the beginning).

        Returns:
            ``Generator``: A generator yielding bytes chunk by chunk

        Example:
            .. code-block:: python

                # Stream the whole media
                async for chunk in app.stream_media(message):
                    print(len(chunk))

                # Stream the first 3 chunks only
                async for chunk in app.stream_media(message, limit=3):
                    print(len(chunk))

                # Stream the rest of the media by skipping the first 3 chunks
                async for chunk in app.stream_media(message, offset=3):
                    print(len(chunk))

                # Stream the last 3 chunks only (negative offset)
                async for chunk in app.stream_media(message, offset=-3):
                    print(len(chunk))
        """
        available_media = (
            "audio",
            "document",
            "photo",
            "sticker",
            "animation",
            "video",
            "voice",
            "video_note",
            "new_chat_photo",
        )

        if isinstance(message, types.Message):
            for kind in available_media:
                media = getattr(message, kind, None)

                if media is not None:
                    break
            else:
                raise ValueError(
                    "This message doesn't contain any downloadable media",
                )
        else:
            media = message

        file_id_str = media if isinstance(media, str) else media.file_id

        file_id_obj = FileId.decode(file_id_str)
        file_size = getattr(media, "file_size", 0)

        if offset < 0:
            if file_size == 0:
                raise ValueError(
                    "Negative offsets are not supported for file ids, pass a Message object instead",
                )

            chunks = math.ceil(file_size / 1024 / 1024)
            offset += chunks

        async for chunk in self.get_file(file_id_obj, file_size, limit, offset):
            yield chunk
