from __future__ import annotations

import pyrogram
from pyrogram import raw


class SellGift:
    async def sell_gift(
        self: pyrogram.Client,
        sender_user_id: int | str,
        message_id: int,
    ) -> bool:
        """Sells a gift received by the current user for Telegram Stars.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            sender_user_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the user that sent the gift.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            message_id (``int``):
                Unique identifier of the message with the gift in the chat with the user.

        Returns:
            ``bool``: On success, True is returned.

        Example:
            .. code-block:: python

                # Convert gift
                app.sell_gift(sender_user_id=user_id, message_id=123)

        """
        peer = await self.resolve_peer(sender_user_id)

        if not isinstance(peer, raw.types.InputPeerUser | raw.types.InputPeerSelf):
            raise ValueError("sender_user_id must belong to a user.")

        return await self.invoke(
            raw.functions.payments.ConvertStarGift(user_id=peer, msg_id=message_id),
        )
