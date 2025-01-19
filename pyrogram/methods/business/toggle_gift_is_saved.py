from __future__ import annotations

import pyrogram
from pyrogram import raw


class ToggleGiftIsSaved:
    async def toggle_gift_is_saved(
        self: pyrogram.Client,
        sender_user_id: int | str,
        message_id: int,
        is_saved: bool,
    ) -> bool:
        """Toggles whether a gift is shown on the current user's profile page.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            sender_user_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target user that sent the gift.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            message_id (``int``):
                Unique message identifier of the message with the gift in the chat with the user.

            is_saved (``bool``):
                Pass True to display the gift on the user's profile page; pass False to remove it from the profile page.

        Returns:
            ``bool``: On success, True is returned.

        Example:
            .. code-block:: python

                # Hide gift
                app.toggle_gift_is_saved(sender_user_id=user_id, message_id=123, is_saved=False)
        """
        peer = await self.resolve_peer(sender_user_id)

        if not isinstance(peer, raw.types.InputPeerUser | raw.types.InputPeerSelf):
            raise ValueError("sender_user_id must belong to a user.")

        return await self.invoke(
            raw.functions.payments.SaveStarGift(
                user_id=peer,
                msg_id=message_id,
                unsave=not is_saved,
            ),
        )
