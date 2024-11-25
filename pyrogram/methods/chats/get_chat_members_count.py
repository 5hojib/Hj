from __future__ import annotations

import pyrogram
from pyrogram import raw


class GetChatMembersCount:
    async def get_chat_members_count(
        self: pyrogram.Client,
        chat_id: int | str,
        join_request: bool = False,
    ) -> int:
        """Get the number of members in a chat.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                You can also use chat public link in form of *t.me/<username>* (str).

            join_request (``bool``, *optional*):
                If True, the count will include the number of users who sent a join request to the chat.

        Returns:
            ``int``: On success, the chat members count is returned.

        Raises:
            ValueError: In case a chat id belongs to user.

        Example:
            .. code-block:: python

                count = await app.get_chat_members_count(chat_id)
                print(count)
        """
        peer = await self.resolve_peer(chat_id)

        if isinstance(peer, raw.types.InputPeerChat):
            r = await self.invoke(raw.functions.messages.GetChats(id=[peer.chat_id]))

            if not join_request:
                return r.chats[0].participants_count
            return r.chats[0].requests_pending
        if isinstance(peer, raw.types.InputPeerChannel):
            r = await self.invoke(
                raw.functions.channels.GetFullChannel(channel=peer),
            )

            if not join_request:
                return r.full_chat.participants_count
            return r.full_chat.requests_pending
        raise ValueError(f'The chat_id "{chat_id}" belongs to a user')
