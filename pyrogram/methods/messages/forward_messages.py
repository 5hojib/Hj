from __future__ import annotations

from typing import TYPE_CHECKING

import pyrogram
from pyrogram import raw, types, utils

if TYPE_CHECKING:
    from collections.abc import Iterable
    from datetime import datetime


class ForwardMessages:
    async def forward_messages(
        self: pyrogram.Client,
        chat_id: int | str,
        from_chat_id: int | str,
        message_ids: int | Iterable[int],
        message_thread_id: int | None = None,
        disable_notification: bool | None = None,
        schedule_date: datetime | None = None,
        protect_content: bool | None = None,
        allow_paid_broadcast: bool | None = None,
        drop_author: bool | None = None,
    ) -> types.Message | list[types.Message]:
        """Forward messages of any kind.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).
                You can also use chat public link in form of *t.me/<username>* (str).

            from_chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the source chat where the original message was sent.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).
                You can also use chat public link in form of *t.me/<username>* (str).

            message_ids (``int`` | Iterable of ``int``):
                An iterable of message identifiers in the chat specified in *from_chat_id* or a single message id.

            message_thread_id (``int``, *optional*):
                Unique identifier of a message thread to which the message belongs.
                for supergroups only

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            schedule_date (:py:obj:`~datetime.datetime`, *optional*):
                Date when the message will be automatically sent.

            protect_content (``bool``, *optional*):
                Protects the contents of the sent message from forwarding and saving.

            allow_paid_broadcast (``bool``, *optional*):
                Pass True to allow the message to ignore regular broadcast limits for a small fee; for bots only.

            drop_author (``bool``, *optional*):
                Forwards messages without quoting the original author

        Returns:
            :obj:`~pyrogram.types.Message` | List of :obj:`~pyrogram.types.Message`: In case *message_ids* was not
            a list, a single message is returned, otherwise a list of messages is returned.

        Example:
            .. code-block:: python

                # Forward a single message
                await app.forward_messages(to_chat, from_chat, 123)

                # Forward multiple messages at once
                await app.forward_messages(to_chat, from_chat, [1, 2, 3])
        """

        is_iterable = not isinstance(message_ids, int)
        message_ids = list(message_ids) if is_iterable else [message_ids]

        r = await self.invoke(
            raw.functions.messages.ForwardMessages(
                to_peer=await self.resolve_peer(chat_id),
                from_peer=await self.resolve_peer(from_chat_id),
                id=message_ids,
                top_msg_id=message_thread_id,
                silent=disable_notification or None,
                random_id=[self.rnd_id() for _ in message_ids],
                schedule_date=utils.datetime_to_timestamp(schedule_date),
                noforwards=protect_content,
                allow_paid_floodskip=allow_paid_broadcast,
                drop_author=drop_author,
            ),
        )

        users = {i.id: i for i in r.users}
        chats = {i.id: i for i in r.chats}

        forwarded_messages = [
            await types.Message._parse(self, i.message, users, chats)
            for i in r.updates
            if isinstance(
                i,
                raw.types.UpdateNewMessage
                | raw.types.UpdateNewChannelMessage
                | raw.types.UpdateNewScheduledMessage,
            )
        ]

        return (
            types.List(forwarded_messages) if is_iterable else forwarded_messages[0]
        )
