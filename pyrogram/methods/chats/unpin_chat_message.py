from __future__ import annotations

import pyrogram
from pyrogram import raw


class UnpinChatMessage:
    async def unpin_chat_message(
        self: pyrogram.Client,
        chat_id: int | str,
        message_id: int = 0,
    ) -> bool:
        """Unpin a message in a group, channel or your own chat.
        You must be an administrator in the chat for this to work and must have the "can_pin_messages" admin
        right in the supergroup or "can_edit_messages" admin right in the channel.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                You can also use chat public link in form of *t.me/<username>* (str).

            message_id (``int``, *optional*):
                Identifier of a message to unpin.
                If not specified, the most recent pinned message (by sending date) will be unpinned.

        Returns:
            ``bool``: True on success.

        Example:
            .. code-block:: python

                await app.unpin_chat_message(chat_id, message_id)
        """
        await self.invoke(
            raw.functions.messages.UpdatePinnedMessage(
                peer=await self.resolve_peer(chat_id),
                id=message_id,
                unpin=True,
            ),
        )

        return True
