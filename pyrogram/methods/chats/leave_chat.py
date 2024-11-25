from __future__ import annotations

import pyrogram
from pyrogram import raw


class LeaveChat:
    async def leave_chat(
        self: pyrogram.Client,
        chat_id: int | str,
        delete: bool = False,
    ):
        """Leave a group chat or channel.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier for the target chat or username of the target channel/supergroup
                (in the format @username).
                You can also use chat public link in form of *t.me/<username>* (str).

            delete (``bool``, *optional*):
                Deletes the group chat dialog after leaving (for simple group chats, not supergroups).
                Defaults to False.

        Example:
            .. code-block:: python

                # Leave chat or channel
                await app.leave_chat(chat_id)

                # Leave basic chat and also delete the dialog
                await app.leave_chat(chat_id, delete=True)
        """
        peer = await self.resolve_peer(chat_id)
        if not self.skip_updates:
            await self.storage.remove_state(chat_id)

        if isinstance(peer, raw.types.InputPeerChannel):
            return await self.invoke(
                raw.functions.channels.LeaveChannel(
                    channel=await self.resolve_peer(chat_id),
                ),
            )
        if isinstance(peer, raw.types.InputPeerChat):
            r = await self.invoke(
                raw.functions.messages.DeleteChatUser(
                    chat_id=peer.chat_id,
                    user_id=raw.types.InputUserSelf(),
                ),
            )

            if delete:
                await self.invoke(
                    raw.functions.messages.DeleteHistory(peer=peer, max_id=0),
                )

            return r
        return None
