from __future__ import annotations

import pyrogram
from pyrogram import raw


class DeleteChatInviteLink:
    async def delete_chat_invite_link(
        self: pyrogram.Client,
        chat_id: int | str,
        invite_link: str,
    ) -> bool:
        """Delete an already revoked invite link.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier for the target chat or username of the target channel/supergroup
                (in the format @username).
                You can also use chat public link in form of *t.me/<username>* (str).

            invite_link (``str``):
                The revoked invite link to delete.

        Returns:
            ``bool``: On success ``True`` is returned.
        """

        return await self.invoke(
            raw.functions.messages.DeleteExportedChatInvite(
                peer=await self.resolve_peer(chat_id),
                link=invite_link,
            ),
        )
