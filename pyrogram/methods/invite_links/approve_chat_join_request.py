from __future__ import annotations

import pyrogram
from pyrogram import raw


class ApproveChatJoinRequest:
    async def approve_chat_join_request(
        self: pyrogram.Client,
        chat_id: int | str,
        user_id: int,
    ) -> bool:
        """Approve a chat join request.

        You must be an administrator in the chat for this to work and must have the *can_invite_users* administrator
        right.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier for the target chat or username of the target channel/supergroup
                (in the format @username).
                You can also use chat public link in form of *t.me/<username>* (str).

            user_id (``int``):
                Unique identifier of the target user.
                You can also use user profile link in form of *t.me/<username>* (str).

        Returns:
            ``bool``: True on success.
        """
        await self.invoke(
            raw.functions.messages.HideChatJoinRequest(
                peer=await self.resolve_peer(chat_id),
                user_id=await self.resolve_peer(user_id),
                approved=True,
            ),
        )

        return True
