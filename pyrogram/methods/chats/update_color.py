from __future__ import annotations

import pyrogram
from pyrogram import enums, raw


class UpdateColor:
    async def update_color(
        self: pyrogram.Client,
        chat_id: int | str,
        color: enums.ReplyColor | enums.ProfileColor,
        background_emoji_id: int | None = None,
    ) -> bool:
        """Update color

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                You can also use chat public link in form of *t.me/<username>* (str).

            color (:obj:`~pyrogram.enums.ReplyColor` | :obj:`~pyrogram.enums.ProfileColor`):
                Color type.
                Profile color can only be set for the user.

            background_emoji_id (``int``, *optional*):
                Unique identifier of the custom emoji.

        Returns:
            ``bool``: On success, in case the passed-in session is authorized, True is returned.

        Example:
            .. code-block:: python

                await app.update_color(chat_id, enums.ReplyColor.RED)
        """
        peer = await self.resolve_peer(chat_id)

        if isinstance(peer, raw.types.InputPeerSelf):
            r = await self.invoke(
                raw.functions.account.UpdateColor(
                    for_profile=isinstance(color, enums.ProfileColor),
                    color=color.value,
                    background_emoji_id=background_emoji_id,
                ),
            )
        else:
            r = await self.invoke(
                raw.functions.channels.UpdateColor(
                    channel=peer,
                    color=color.value,
                    background_emoji_id=background_emoji_id,
                ),
            )

        return bool(r)
