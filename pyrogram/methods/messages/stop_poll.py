from __future__ import annotations

import pyrogram
from pyrogram import raw, types


class StopPoll:
    async def stop_poll(
        self: pyrogram.Client,
        chat_id: int | str,
        message_id: int,
        reply_markup: types.InlineKeyboardMarkup = None,
        business_connection_id: str | None = None,
    ) -> types.Poll:
        """Stop a poll which was sent by you.

        Stopped polls can't be reopened and nobody will be able to vote in it anymore.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).
                You can also use chat public link in form of *t.me/<username>* (str).

            message_id (``int``):
                Identifier of the original message with the poll.

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup`, *optional*):
                An InlineKeyboardMarkup object.

            business_connection_id (``str``, *optional*):
                Unique identifier of the business connection.

        Returns:
            :obj:`~pyrogram.types.Poll`: On success, the stopped poll with the final results is returned.

        Example:
            .. code-block:: python

                await app.stop_poll(chat_id, message_id)
        """
        poll = (await self.get_messages(chat_id, message_id)).poll

        rpc = raw.functions.messages.EditMessage(
            peer=await self.resolve_peer(chat_id),
            id=message_id,
            media=raw.types.InputMediaPoll(
                poll=raw.types.Poll(
                    id=int(poll.id),
                    closed=True,
                    question="",
                    answers=[],
                ),
            ),
            reply_markup=await reply_markup.write(self) if reply_markup else None,
        )
        if business_connection_id is not None:
            r = await self.invoke(
                raw.functions.InvokeWithBusinessConnection(
                    connection_id=business_connection_id,
                    query=rpc,
                ),
            )
        else:
            r = await self.invoke(rpc)

        return await types.Poll._parse(self, r.updates[0], r.users)
