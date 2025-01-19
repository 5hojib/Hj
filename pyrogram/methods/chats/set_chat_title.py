from __future__ import annotations

import pyrogram
from pyrogram import raw


class SetChatTitle:
    async def set_chat_title(
        self: pyrogram.Client,
        chat_id: int | str,
        title: str,
    ) -> bool:
        """Change the title of a chat.
        Titles can't be changed for private chats.
        You must be an administrator in the chat for this to work and must have the appropriate admin rights.

        Note:
            In regular groups (non-supergroups), this method will only work if the "All Members Are Admins"
            setting is off.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                You can also use chat public link in form of *t.me/<username>* (str).

            title (``str``):
                New chat title, 1-255 characters.

        Returns:
            ``bool``: True on success.

        Raises:
            ValueError: In case a chat id belongs to user.

        Example:
            .. code-block:: python

                await app.set_chat_title(chat_id, "New Title")
        """
        peer = await self.resolve_peer(chat_id)

        if isinstance(peer, raw.types.InputPeerChat):
            await self.invoke(
                raw.functions.messages.EditChatTitle(
                    chat_id=peer.chat_id,
                    title=title,
                ),
            )
        elif isinstance(peer, raw.types.InputPeerChannel):
            await self.invoke(
                raw.functions.channels.EditTitle(channel=peer, title=title),
            )
        else:
            raise ValueError(f'The chat_id "{chat_id}" belongs to a user')

        return True
