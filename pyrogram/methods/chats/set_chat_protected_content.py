from __future__ import annotations

import pyrogram
from pyrogram import raw


class SetChatProtectedContent:
    async def set_chat_protected_content(
        self: pyrogram.Client,
        chat_id: int | str,
        enabled: bool,
    ) -> bool:
        """Set the chat protected content setting.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                You can also use chat public link in form of *t.me/<username>* (str).

            enabled (``bool``):
                Pass True to enable the protected content setting, False to disable.

        Returns:
            ``bool``: On success, True is returned.
        """

        await self.invoke(
            raw.functions.messages.ToggleNoForwards(
                peer=await self.resolve_peer(chat_id),
                enabled=enabled,
            ),
        )

        return True
