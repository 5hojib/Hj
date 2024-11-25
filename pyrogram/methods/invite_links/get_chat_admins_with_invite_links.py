from __future__ import annotations

import pyrogram
from pyrogram import raw, types


class GetChatAdminsWithInviteLinks:
    async def get_chat_admins_with_invite_links(
        self: pyrogram.Client,
        chat_id: int | str,
    ):
        """Get the list of the administrators that have exported invite links in a chat.

        You must be the owner of a chat for this to work.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier for the target chat or username of the target channel/supergroup
                (in the format @username).
                You can also use chat public link in form of *t.me/<username>* (str).

        Returns:
            List of :obj:`~pyrogram.types.ChatAdminWithInviteLink`: On success, the list of admins that have exported
            invite links is returned.
        """
        r = await self.invoke(
            raw.functions.messages.GetAdminsWithInvites(
                peer=await self.resolve_peer(chat_id),
            ),
        )

        users = {i.id: i for i in r.users}

        return types.List(
            types.ChatAdminWithInviteLinks._parse(self, admin, users)
            for admin in r.admins
        )
