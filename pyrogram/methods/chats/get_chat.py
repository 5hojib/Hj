from __future__ import annotations

import pyrogram
from pyrogram import raw, types, utils


class GetChat:
    async def get_chat(
        self: pyrogram.Client,
        chat_id: int | str,
    ) -> types.Chat | types.ChatPreview:
        """Get up to date information about a chat.

        Information include current name of the user for one-on-one conversations, current username of a user, group or
        channel, etc.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                Unique identifier for the target chat in form of a *t.me/joinchat/* or *t.me/<username>* link link,
                identifier (int) or username of the target channel/supergroup (in the format @username).
                You can also use chat public link in form of *t.me/<username>* (str).

        Returns:
            :obj:`~pyrogram.types.Chat` | :obj:`~pyrogram.types.ChatPreview`: On success, if you've already joined the chat, a chat object is returned,
            otherwise, a chat preview object is returned.

        Raises:
            ValueError: In case the chat invite link points to a chat you haven't joined yet.

        Example:
            .. code-block:: python

                chat = await app.get_chat("pyrogram")
                print(chat)
        """
        match = self.INVITE_LINK_RE.match(str(chat_id))

        if match:
            r = await self.invoke(
                raw.functions.messages.CheckChatInvite(hash=match.group(1)),
            )

            if isinstance(r, raw.types.ChatInvite):
                return types.ChatPreview._parse(self, r)

            await self.fetch_peers([r.chat])

            if isinstance(r.chat, raw.types.Chat):
                chat_id = -r.chat.id

            if isinstance(r.chat, raw.types.Channel):
                chat_id = utils.get_channel_id(r.chat.id)

        peer = await self.resolve_peer(chat_id)

        if isinstance(peer, raw.types.InputPeerChannel):
            r = await self.invoke(
                raw.functions.channels.GetFullChannel(channel=peer),
            )
        elif isinstance(peer, raw.types.InputPeerUser | raw.types.InputPeerSelf):
            r = await self.invoke(raw.functions.users.GetFullUser(id=peer))
        else:
            r = await self.invoke(
                raw.functions.messages.GetFullChat(chat_id=peer.chat_id),
            )

        return await types.Chat._parse_full(self, r)
