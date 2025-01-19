from __future__ import annotations

import pyrogram
from pyrogram import raw


class UpdatePersonalChat:
    async def update_personal_chat(
        self: pyrogram.Client,
        chat_id: int | str,
    ) -> bool:
        """Update your birthday details.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int``):
                Unique identifier (int) of the target channel.
                You can also use channel public link in form of *t.me/<username>* (str).

        Returns:
            ``bool``: True on success.

        Example:
            .. code-block:: python

                # Update your personal chat
                await app.update_personal_chat(chat_id=-1001234567890)
        """
        chat = await self.resolve_peer(chat_id)
        r = await self.invoke(
            raw.functions.account.UpdatePersonalChannel(channel=chat),
        )
        return bool(r)
