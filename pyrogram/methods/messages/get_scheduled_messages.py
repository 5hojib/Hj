from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import pyrogram
from pyrogram import raw, types, utils

if TYPE_CHECKING:
    from collections.abc import Iterable

log = logging.getLogger(__name__)


class GetScheduledMessages:
    async def get_scheduled_messages(
        self: pyrogram.Client,
        chat_id: int | str,
        message_ids: int | Iterable[int],
    ) -> types.Message | list[types.Message]:
        """Get one or more scheduled messages from a chat by using message identifiers.
        You can retrieve up to 200 messages at once.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).
                You can also use chat public link in form of *t.me/<username>* (str).
            message_ids (``int`` | Iterable of ``int``):
                Pass a single message identifier or an iterable of message ids (as integers) to get the content of the
                message themselves.

        Returns:
            :obj:`~pyrogram.types.Message` | List of :obj:`~pyrogram.types.Message`: In case *message_ids* was not
            a list, a single message is returned, otherwise a list of messages is returned.

        Example:
            .. code-block:: python

                # Get one scheduled message
                await app.get_scheduled_message(chat_id, 12345)
                # Get more than one scheduled message (list of messages)
                await app.get_scheduled_message(chat_id, [12345, 12346])

        Raises:
            ValueError: In case of invalid arguments.
        """

        if message_ids is None:
            raise ValueError("No argument supplied. Pass message_ids")

        peer = await self.resolve_peer(chat_id)

        is_iterable = not isinstance(message_ids, int)
        ids = list(message_ids) if is_iterable else [message_ids]

        rpc = raw.functions.messages.GetScheduledMessages(peer=peer, id=ids)

        r = await self.invoke(rpc, sleep_threshold=-1)

        messages = await utils.parse_messages(self, r)

        return messages if is_iterable else messages[0] if messages else None
