from __future__ import annotations

import pyrogram
from pyrogram import raw, types


class GetChatInviteLink:
    async def get_chat_invite_link(
        self: pyrogram.Client,
        chat_id: int | str,
        invite_link: str,
    ) -> types.ChatInviteLink:
        """Get detailed information about a chat invite link.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier for the target chat or username of the target channel/supergroup
                (in the format @username).
                You can also use chat public link in form of *t.me/<username>* (str).

            invite_link (str):
                The invite link.

        Returns:
            :obj:`~pyrogram.types.ChatInviteLink`: On success, the invite link is returned.
        """
        r = await self.invoke(
            raw.functions.messages.GetExportedChatInvite(
                peer=await self.resolve_peer(chat_id),
                link=invite_link,
            ),
        )

        users = {i.id: i for i in r.users}

        return types.ChatInviteLink._parse(self, r.invite, users)
