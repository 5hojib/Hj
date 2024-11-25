from __future__ import annotations

from typing import TYPE_CHECKING

import pyrogram
from pyrogram import raw, types, utils

if TYPE_CHECKING:
    from datetime import datetime


class CreateChatInviteLink:
    async def create_chat_invite_link(
        self: pyrogram.Client,
        chat_id: int | str,
        name: str | None = None,
        expire_date: datetime | None = None,
        member_limit: int | None = None,
        creates_join_request: bool | None = None,
    ) -> types.ChatInviteLink:
        """Create an additional invite link for a chat.

        You must be an administrator in the chat for this to work and must have the appropriate admin rights.

        The link can be revoked using the method :meth:`~pyrogram.Client.revoke_chat_invite_link`.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier for the target chat or username of the target channel/supergroup
                (in the format @username).
                You can also use chat public link in form of *t.me/<username>* (str).

            name (``str``, *optional*):
                Invite link name.

            expire_date (:py:obj:`~datetime.datetime`, *optional*):
                Point in time when the link will expire.
                Defaults to None (no expiration date).

            member_limit (``int``, *optional*):
                Maximum number of users that can be members of the chat simultaneously after joining the chat via
                this invite link; 1-99999.
                Defaults to None (no member limit).

            creates_join_request (``bool``, *optional*):
                True, if users joining the chat via the link need to be approved by chat administrators.
                If True, member_limit can't be specified.

        Returns:
            :obj:`~pyrogram.types.ChatInviteLink`: On success, the new invite link is returned.

        Example:
            .. code-block:: python

                # Create a new link without limits
                link = await app.create_chat_invite_link(chat_id)

                # Create a new link for up to 3 new users
                link = await app.create_chat_invite_link(chat_id, member_limit=3)
        """
        r = await self.invoke(
            raw.functions.messages.ExportChatInvite(
                peer=await self.resolve_peer(chat_id),
                expire_date=utils.datetime_to_timestamp(expire_date),
                usage_limit=member_limit,
                title=name,
                request_needed=creates_join_request,
            ),
        )

        return types.ChatInviteLink._parse(self, r)
