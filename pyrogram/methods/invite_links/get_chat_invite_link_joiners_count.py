from __future__ import annotations

import pyrogram
from pyrogram import raw


class GetChatInviteLinkJoinersCount:
    async def get_chat_invite_link_joiners_count(
        self: pyrogram.Client,
        chat_id: int | str,
        invite_link: str,
    ) -> int:
        """Get the count of the members who joined the chat with the invite link.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier for the target chat or username of the target channel/supergroup
                (in the format @username).
                You can also use chat public link in form of *t.me/<username>* (str).

            invite_link (str):
                The invite link.

        Returns:
            ``int``: On success, the joined chat members count is returned.
        """
        r = await self.invoke(
            raw.functions.messages.GetChatInviteImporters(
                peer=await self.resolve_peer(chat_id),
                link=invite_link,
                limit=1,
                offset_date=0,
                offset_user=raw.types.InputUserEmpty(),
            ),
        )

        return r.count
