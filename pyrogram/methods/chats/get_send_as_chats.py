from __future__ import annotations

import pyrogram
from pyrogram import raw, types


class GetSendAsChats:
    async def get_send_as_chats(
        self: pyrogram.Client,
        chat_id: int | str,
    ) -> list[types.Chat]:
        """Get the list of "send_as" chats available.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                You can also use chat public link in form of *t.me/<username>* (str).

        Returns:
            list[:obj:`~pyrogram.types.Chat`]: The list of chats.

        Example:
            .. code-block:: python

                chats = await app.get_send_as_chats(chat_id)
                print(chats)
        """
        r = await self.invoke(
            raw.functions.channels.GetSendAs(peer=await self.resolve_peer(chat_id)),
        )

        users = {u.id: u for u in r.users}
        chats = {c.id: c for c in r.chats}

        send_as_chats = types.List()

        for p in r.peers:
            if isinstance(p.peer, raw.types.PeerUser):
                send_as_chats.append(
                    types.Chat._parse_chat(self, users[p.peer.user_id]),
                )
            else:
                send_as_chats.append(
                    types.Chat._parse_chat(self, chats[p.peer.channel_id]),
                )

        return send_as_chats
