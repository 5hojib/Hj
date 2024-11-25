from __future__ import annotations

import re
from pathlib import Path

import pyrogram
from pyrogram import raw, types
from pyrogram.file_id import FileId


class CreateStickerSet:
    async def create_sticker_set(
        self: pyrogram.Client,
        user_id: int | str,
        title: str,
        short_name: str,
        sticker: str,
        emoji: str = "🤔",
        masks: bool | None = None,
    ) -> types.Message | None:
        """Create a new stickerset.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            user_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the Stickerset owner.
                For you yourself you can simply use "me" or "self" (users only).

            title (``str``):
                Stickerset name, 1-64 chars

            short_name (``str``, *optional*):
                Short name of sticker set, to be used in sticker deep links.
                Can contain only english letters, digits and underscores.
                Must begin with a letter, can't contain consecutive underscores and, if called by a bot, must end in "_by_<bot_username>".
                <bot_username> is case insensitive. 1-64 characters.

            sticker (``str``):
                sticker to add.
                Pass a file_id as string to send a file that exists on the Telegram servers.

            emoji (``str``, *optional*):
                Associated emoji.
                default to "🤔"

            masks (``bool``, *optional*):
                Whether this is a mask stickerset.

        Returns:
            :obj:`~pyrogram.types.StickerSet` | ``None``: On success, the StickerSet is returned.

        Example:
            .. code-block:: python

                # Send document by uploading from local file
                await app.create_sticker_set("me", "My First Pack", "myfirstpack", "AAjjHjk")
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
            raw.functions.stickers.CreateStickerSet(
                user_id=await self.resolve_peer(user_id),
                title=title,
                short_name=short_name,
                stickers=[
                    raw.types.InputStickerSetItem(document=media, emoji=emoji),
                ],
                masks=masks,
            ),
        )

        return types.StickerSet._parse(r.set)
