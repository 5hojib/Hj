from __future__ import annotations

import pyrogram
from pyrogram import raw, types


class GetStickerSet:
    async def get_sticker_set(
        self: pyrogram.Client,
        set_short_name: str,
    ) -> types.StickerSet:
        """Get info about a stickerset.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            set_short_name (``str``):
               Stickerset shortname.

        Returns:
            :obj:`~pyrogram.types.StickerSet`: On success, the StickerSet information is returned.

        Example:
            .. code-block:: python

                await app.get_sticker_set("mypack1")
        """
        r = await self.invoke(
            raw.functions.messages.GetStickerSet(
                stickerset=raw.types.InputStickerSetShortName(
                    short_name=set_short_name,
                ),
                hash=0,
            ),
        )

        return types.StickerSet._parse(r.set)
