from __future__ import annotations

import pyrogram
from pyrogram import raw, types


class SetChatMenuButton:
    async def set_chat_menu_button(
        self: pyrogram.Client,
        chat_id: int | str | None = None,
        menu_button: types.MenuButton = None,
    ) -> bool:
        """Change the bot's menu button in a private chat, or the default menu button.

        .. include:: /_includes/usable-by/bots.rst

        Parameters:
            chat_id (``int`` | ``str``, *optional*):
                Unique identifier (int) or username (str) of the target chat.
                If not specified, default bot's menu button will be changed.

            menu_button (:obj:`~pyrogram.types.MenuButton`, *optional*):
                The new bot's menu button.
                Defaults to :obj:`~pyrogram.types.MenuButtonDefault`.
        """

        await self.invoke(
            raw.functions.bots.SetBotMenuButton(
                user_id=await self.resolve_peer(chat_id or "me"),
                button=(
                    (await menu_button.write(self))
                    if menu_button
                    else (await types.MenuButtonDefault().write(self))
                ),
            ),
        )

        return True
