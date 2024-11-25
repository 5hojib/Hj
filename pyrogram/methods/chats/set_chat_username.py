from __future__ import annotations

import pyrogram
from pyrogram import raw


class SetChatUsername:
    async def set_chat_username(
        self: pyrogram.Client,
        chat_id: int | str,
        username: str | None,
    ) -> bool:
        """Set a channel or a supergroup username.

        To set your own username (for users only, not bots) you can use :meth:`~pyrogram.Client.set_username`.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int`` | ``str``)
                Unique identifier (int) or username (str) of the target chat.
                You can also use chat public link in form of *t.me/<username>* (str).

            username (``str`` | ``None``):
                Username to set. Pass "" (empty string) or None to remove the username.

        Returns:
            ``bool``: True on success.

        Raises:
            ValueError: In case a chat id belongs to a user or chat.

        Example:
            .. code-block:: python

                await app.set_chat_username(chat_id, "new_username")
        """

        peer = await self.resolve_peer(chat_id)

        if isinstance(peer, raw.types.InputPeerChannel):
            return bool(
                await self.invoke(
                    raw.functions.channels.UpdateUsername(
                        channel=peer,
                        username=username or "",
                    ),
                ),
            )
        raise ValueError(f'The chat_id "{chat_id}" belongs to a user or chat')
