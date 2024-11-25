from __future__ import annotations

import logging

import pyrogram
from pyrogram import raw, types

log = logging.getLogger(__name__)


class SendPaidReaction:
    async def send_paid_reaction(
        self: pyrogram.Client,
        chat_id: int | str,
        message_id: int,
        star_count: int | None = None,
        is_anonymous: bool = False,
    ) -> types.MessageReactions:
        """Adds the paid message reaction to a message.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            message_id (``int``):
                Identifier of the target message. If the message belongs to a media group, the reaction is set to the first non-deleted message in the group instead.

            star_count (``int``, *optional*):
                Number of Telegram Stars to be used for the reaction; 1-2500.

            is_anonymous (``bool``, *optional*):
                Pass True to make paid reaction of the user on the message anonymous; pass False to make the user's profile visible among top reactors.
                Defaults to False.

        Returns:
            On success, :obj:`~pyrogram.types.MessageReactions`: is returned.

        Example:
            .. code-block:: python

                # Add a paid reaction to a message
                await app.add_paid_message_reaction(chat_id, message_id, 1, False)
        """

        r = await self.invoke(
            raw.functions.messages.SendPaidReaction(
                peer=await self.resolve_peer(chat_id),
                msg_id=message_id,
                random_id=self.rnd_id(),
                count=star_count,
                private=is_anonymous,
            ),
        )
        users = {i.id: i for i in r.users}
        for i in r.updates:
            if isinstance(i, raw.types.UpdateMessageReactions):
                return types.MessageReactions._parse(self, i.reactions, users)
        # TODO
        return r
