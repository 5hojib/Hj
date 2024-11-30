from __future__ import annotations

from typing import TYPE_CHECKING

import pyrogram
from pyrogram import raw, types, utils

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator
    from datetime import datetime


async def get_chunk(
    *,
    client: pyrogram.Client,
    chat_id: int | str,
    limit: int = 0,
    offset: int = 0,
    from_message_id: int = 0,
    from_date: datetime | None = None,
    min_id: int = 0,
    max_id: int = 0,
):
    if from_date is None:
        from_date = utils.zero_datetime()
    messages = await client.invoke(
        raw.functions.messages.GetHistory(
            peer=await client.resolve_peer(chat_id),
            offset_id=from_message_id,
            offset_date=utils.datetime_to_timestamp(from_date),
            add_offset=offset,
            limit=limit,
            max_id=max_id,
            min_id=min_id,
            hash=0,
        ),
        sleep_threshold=60,
    )

    return await utils.parse_messages(client, messages)


class GetChatHistory:
    async def get_chat_history(
        self: pyrogram.Client,
        chat_id: int | str,
        limit: int = 0,
        offset: int = 0,
        offset_id: int = 0,
        offset_date: datetime | None = None,
        min_id: int = 0,
        max_id: int = 0,
    ) -> AsyncGenerator[types.Message, None] | None:
        """Get messages from a chat history.

        The messages are returned in reverse chronological order.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).
                You can also use chat public link in form of *t.me/<username>* (str).

            limit (``int``, *optional*):
                Limits the number of messages to be retrieved.
                By default, no limit is applied and all messages are returned.

            offset (``int``, *optional*):
                Sequential number of the first message to be returned..
                Negative values are also accepted and become useful in case you set offset_id or offset_date.

            offset_id (``int``, *optional*):
                Identifier of the first message to be returned.

            offset_date (:py:obj:`~datetime.datetime`, *optional*):
                Pass a date as offset to retrieve only older messages starting from that date.

            min_id: (``int``, *optional*):
                The minimum message id. you will not get any message which have id smaller than min_id.

            max_id: (``int``, *optional*):
                The maximum message id. you will not get any message which have id greater than max_id.

        Returns:
            ``Generator``: A generator yielding :obj:`~pyrogram.types.Message` objects.

        Example:
            .. code-block:: python

                async for message in app.get_chat_history(chat_id):
                    print(message.text)
        """
        if offset_date is None:
            offset_date = utils.zero_datetime()
        current = 0
        total = limit or (1 << 31) - 1
        limit = min(100, total)

        while True:
            messages = await get_chunk(
                client=self,
                chat_id=chat_id,
                limit=limit,
                offset=offset,
                from_message_id=offset_id,
                from_date=offset_date,
                min_id=min_id,
                max_id=max_id,
            )

            if not messages:
                return

            offset_id = messages[-1].id

            for message in messages:
                yield message

                current += 1

                if current >= total:
                    return
