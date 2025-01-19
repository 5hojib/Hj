from __future__ import annotations

import pyrogram
from pyrogram import raw


class SetUsername:
    async def set_username(self: pyrogram.Client, username: str | None) -> bool:
        """Set your own username.

        This method only works for users, not bots. Bot usernames must be changed via Bot Support or by recreating
        them from scratch using BotFather. To set a channel or supergroup username you can use
        :meth:`~pyrogram.Client.set_chat_username`.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            username (``str`` | ``None``):
                Username to set. "" (empty string) or None to remove it.

        Returns:
            ``bool``: True on success.

        Example:
            .. code-block:: python

                await app.set_username("new_username")
        """

        return bool(
            await self.invoke(
                raw.functions.account.UpdateUsername(username=username or ""),
            ),
        )
