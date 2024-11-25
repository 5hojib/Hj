from __future__ import annotations

import pyrogram
from pyrogram import raw, types


class RetractVote:
    async def retract_vote(
        self: pyrogram.Client,
        chat_id: int | str,
        message_id: int,
    ) -> types.Poll:
        """Retract your vote in a poll.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).
                You can also use chat public link in form of *t.me/<username>* (str).

            message_id (``int``):
                Identifier of the original message with the poll.

        Returns:
            :obj:`~pyrogram.types.Poll`: On success, the poll with the retracted vote is returned.

        Example:
            .. code-block:: python

                await app.retract_vote(chat_id, message_id)
        """
        r = await self.invoke(
            raw.functions.messages.SendVote(
                peer=await self.resolve_peer(chat_id),
                msg_id=message_id,
                options=[],
            ),
        )

        return await types.Poll._parse(self, r.updates[0], r.users)
