from __future__ import annotations

import pyrogram
from pyrogram import raw, types


class GetCustomEmojiStickers:
    async def get_custom_emoji_stickers(
        self: pyrogram.Client,
        custom_emoji_ids: int | list[int],
    ) -> types.Sticker | list[types.Sticker]:
        """Get information about custom emoji stickers by their identifiers.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            custom_emoji_ids (:obj:`int` | :obj:`list[int]`):
                Custom emoji ID.
                At most 200 custom emoji identifiers can be specified.

        Returns:
            :obj: `~pyrogram.types.Sticker` | List of :obj:`~pyrogram.types.Sticker`: In case *custom_emoji_ids* was not
             a list, a single sticker is returned, otherwise a list of stickers is returned.
        """
        is_list = isinstance(custom_emoji_ids, list)
        custom_emoji_ids = [custom_emoji_ids] if not is_list else custom_emoji_ids

        result = await self.invoke(
            raw.functions.messages.GetCustomEmojiDocuments(
                document_id=custom_emoji_ids,
            ),
        )

        stickers = pyrogram.types.List()
        for item in result:
            attributes = {type(i): i for i in item.attributes}
            sticker = await types.Sticker._parse(self, item, attributes)
            stickers.append(sticker)

        return stickers if is_list else stickers[0]
