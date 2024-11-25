from __future__ import annotations

import re
from pathlib import Path

import pyrogram
from pyrogram import raw, types
from pyrogram.file_id import FileId


class AddStickerToSet:
    async def add_sticker_to_set(
        self: pyrogram.Client,
        set_short_name: str,
        sticker: str,
        emoji: str = "🤔",
    ) -> types.StickerSet:
        """Add a sticker to stickerset.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            set_short_name (``str``):
               Stickerset shortname.

            sticker (``str``):
                sticker to add.
                Pass a file_id as string to send a file that exists on the Telegram servers.

            emoji (``str``, *optional*):
                Associated emoji.
                default to "🤔"

        Returns:
            :obj:`~pyrogram.types.StickerSet`: On success, the StickerSet information is returned.

        Example:
            .. code-block:: python

                await app.add_sticker_to_set("mypack1", "AsJiasp")
        """

        if isinstance(sticker, str):
            if Path(sticker).is_file() or re.match("^https?://", sticker):
                raise ValueError("file_id is invalid!")
            decoded = FileId.decode(sticker)
            media = raw.types.InputDocument(
                id=decoded.media_id,
                access_hash=decoded.access_hash,
                file_reference=decoded.file_reference,
            )
        else:
            raise ValueError("file_id is invalid!")

        r = await self.invoke(
            raw.functions.stickers.AddStickerToSet(
                stickerset=raw.types.InputStickerSetShortName(
                    short_name=set_short_name,
                ),
                sticker=raw.types.InputStickerSetItem(document=media, emoji=emoji),
            ),
        )

        return types.StickerSet._parse(r.set)
