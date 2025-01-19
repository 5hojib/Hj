from __future__ import annotations

import pyrogram
from pyrogram import raw, types


class SetEmojiStatus:
    async def set_emoji_status(
        self: pyrogram.Client,
        emoji_status: types.EmojiStatus | None = None,
    ) -> bool:
        """Set the emoji status.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            emoji_status (:obj:`~pyrogram.types.EmojiStatus`, *optional*):
                The emoji status to set. None to remove.

        Returns:
            ``bool``: On success, True is returned.

        Example:
            .. code-block:: python

                from pyrogram import types

                await app.set_emoji_status(types.EmojiStatus(custom_emoji_id=1234567890987654321))
        """
        await self.invoke(
            raw.functions.account.UpdateEmojiStatus(
                emoji_status=(
                    emoji_status.write()
                    if emoji_status
                    else raw.types.EmojiStatusEmpty()
                ),
            ),
        )

        return True
