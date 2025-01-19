from __future__ import annotations

import pyrogram
from pyrogram import raw


class ApproveAllChatJoinRequests:
    async def approve_all_chat_join_requests(
        self: pyrogram.Client,
        chat_id: int | str,
        invite_link: str | None = None,
    ) -> bool:
        """Approve all pending join requests in a chat.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier for the target chat or username of the target channel/supergroup
                (in the format @username).
                You can also use chat public link in form of *t.me/<username>* (str).

            invite_link (``str``, *optional*):
                Pass an invite link to approve only its join requests.
                By default, all join requests are approved.

        Returns:
            ``bool``: True on success.
        """
        await self.invoke(
            raw.functions.messages.HideAllChatJoinRequests(
                peer=await self.resolve_peer(chat_id),
                approved=True,
                link=invite_link,
            ),
        )

        return True
