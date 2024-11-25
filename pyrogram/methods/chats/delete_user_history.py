from __future__ import annotations

import pyrogram
from pyrogram import raw


class DeleteUserHistory:
    async def delete_user_history(
        self: pyrogram.Client,
        chat_id: int | str,
        user_id: int | str,
    ) -> bool:
        """Delete all messages sent by a certain user in a supergroup.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                You can also use chat public link in form of *t.me/<username>* (str).

            user_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the user whose messages will be deleted.
                You can also use user profile link in form of *t.me/<username>* (str).

        Returns:
            ``bool``: True on success, False otherwise.
        """

        r = await self.invoke(
            raw.functions.channels.DeleteParticipantHistory(
                channel=await self.resolve_peer(chat_id),
                participant=await self.resolve_peer(user_id),
            ),
        )

        # Deleting messages you don't have right onto won't raise any error.
        # Check for pts_count, which is 0 in case deletes fail.
        return bool(r.pts_count)
