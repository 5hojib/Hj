from __future__ import annotations

import pyrogram
from pyrogram import raw


class UnbanChatMember:
    async def unban_chat_member(
        self: pyrogram.Client,
        chat_id: int | str,
        user_id: int | str,
    ) -> bool:
        """Unban a previously banned user in a supergroup or channel.
        The user will **not** return to the group or channel automatically, but will be able to join via link, etc.
        You must be an administrator for this to work.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                You can also use chat public link in form of *t.me/<username>* (str).

            user_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target user.
                For a contact that exists in your Telegram address book you can use his phone number (str).

        Returns:
            ``bool``: True on success.

        Example:
            .. code-block:: python

                # Unban chat member right now
                await app.unban_chat_member(chat_id, user_id)
        """
        await self.invoke(
            raw.functions.channels.EditBanned(
                channel=await self.resolve_peer(chat_id),
                participant=await self.resolve_peer(user_id),
                banned_rights=raw.types.ChatBannedRights(until_date=0),
            ),
        )

        return True
