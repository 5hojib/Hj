from __future__ import annotations

import pyrogram
from pyrogram import raw, types


class GetChatMenuButton:
    async def get_chat_menu_button(
        self: pyrogram.Client,
        chat_id: int | str | None = None,
    ) -> types.MenuButton:
        """Get the current value of the bot's menu button in a private chat, or the default menu button.

        .. include:: /_includes/usable-by/bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                You can also use user profile/chat public link in form of *t.me/<username>* (str).
                If not specified, default bot's menu button will be returned.
        """

        if chat_id:
            r = await self.invoke(
                raw.functions.bots.GetBotMenuButton(
                    user_id=await self.resolve_peer(chat_id),
                ),
            )
        else:
            r = (
                await self.invoke(
                    raw.functions.users.GetFullUser(id=raw.types.InputUserSelf()),
                )
            ).full_user.bot_info.menu_button

        if isinstance(r, raw.types.BotMenuButtonCommands):
            return types.MenuButtonCommands()

        if isinstance(r, raw.types.BotMenuButtonDefault):
            return types.MenuButtonDefault()

        if isinstance(r, raw.types.BotMenuButton):
            return types.MenuButtonWebApp(
                text=r.text,
                web_app=types.WebAppInfo(url=r.url),
            )
        return None
