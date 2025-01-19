from __future__ import annotations

import pyrogram
from pyrogram import raw


class SetChatDescription:
    async def set_chat_description(
        self: pyrogram.Client,
        chat_id: int | str,
        description: str,
    ) -> bool:
        """Change the description of a supergroup or a channel.
        You must be an administrator in the chat for this to work and must have the appropriate admin rights.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                You can also use chat public link in form of *t.me/<username>* (str).

            description (``str``):
                New chat description, 0-255 characters.

        Returns:
            ``bool``: True on success.

        Raises:
            ValueError: if a chat_id doesn't belong to a supergroup or a channel.

        Example:
            .. code-block:: python

                await app.set_chat_description(chat_id, "New Description")
        """
        peer = await self.resolve_peer(chat_id)

        if isinstance(
            peer,
            raw.types.InputPeerChannel | raw.types.InputPeerChat,
        ):
            await self.invoke(
                raw.functions.messages.EditChatAbout(peer=peer, about=description),
            )
        else:
            raise ValueError(f'The chat_id "{chat_id}" belongs to a user')

        return True
