from __future__ import annotations

import pyrogram
from pyrogram import raw


class SetSendAsChat:
    async def set_send_as_chat(
        self: pyrogram.Client,
        chat_id: int | str,
        send_as_chat_id: int | str,
    ) -> bool:
        """Set the default "send_as" chat for a chat.

        Use :meth:`~pyrogram.Client.get_send_as_chats` to get all the "send_as" chats available for use.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                You can also use chat public link in form of *t.me/<username>* (str).

            send_as_chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the send_as chat.
                You can also use chat public link in form of *t.me/<username>* (str).

        Returns:
            ``bool``: On success, true is returned

        Example:
            .. code-block:: python

                await app.set_send_as_chat(chat_id, send_as_chat_id)
        """
        return await self.invoke(
            raw.functions.messages.SaveDefaultSendAs(
                peer=await self.resolve_peer(chat_id),
                send_as=await self.resolve_peer(send_as_chat_id),
            ),
        )
