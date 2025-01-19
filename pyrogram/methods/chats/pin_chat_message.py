from __future__ import annotations

import pyrogram
from pyrogram import raw, types


class PinChatMessage:
    async def pin_chat_message(
        self: pyrogram.Client,
        chat_id: int | str,
        message_id: int,
        disable_notification: bool = False,
        both_sides: bool = False,
    ) -> types.Message:
        """Pin a message in a group, channel or your own chat.
        You must be an administrator in the chat for this to work and must have the "can_pin_messages" admin right in
        the supergroup or "can_edit_messages" admin right in the channel.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                You can also use chat public link in form of *t.me/<username>* (str).

            message_id (``int``):
                Identifier of a message to pin.

            disable_notification (``bool``, *optional*):
                Pass True, if it is not necessary to send a notification to all chat members about the new pinned
                message. Notifications are always disabled in channels.

            both_sides (``bool``, *optional*):
                Pass True to pin the message for both sides (you and recipient).
                Applicable to private chats only. Defaults to False.

        Returns:
            :obj:`~pyrogram.types.Message`: On success, the service message is returned.

        Example:
            .. code-block:: python

                # Pin with notification
                await app.pin_chat_message(chat_id, message_id)

                # Pin without notification
                await app.pin_chat_message(chat_id, message_id, disable_notification=True)
        """
        r = await self.invoke(
            raw.functions.messages.UpdatePinnedMessage(
                peer=await self.resolve_peer(chat_id),
                id=message_id,
                silent=disable_notification or None,
                pm_oneside=not both_sides or None,
            ),
        )

        users = {u.id: u for u in r.users}
        chats = {c.id: c for c in r.chats}

        for i in r.updates:
            if isinstance(
                i,
                raw.types.UpdateNewMessage | raw.types.UpdateNewChannelMessage,
            ):
                return await types.Message._parse(self, i.message, users, chats)
        return None
