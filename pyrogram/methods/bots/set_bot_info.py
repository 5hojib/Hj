from __future__ import annotations

import pyrogram
from pyrogram import raw


class SetBotInfo:
    async def set_bot_info(
        self: pyrogram.Client,
        lang_code: str,
        bot: int | str | None = None,
        name: str | None = None,
        about: str | None = None,
        description: str | None = None,
    ) -> bool:
        """Get the bot info in given language.

        .. include:: /_includes/usable-by/users-bots.rst

        Note:
            For normal bot you can only use this method to self.
            For userbot you can only use this method if you are the owner of target bot.

        Parameters:
            lang_code ``str``:
                A two-letter ISO 639-1 language code.
            bot (``int`` | ``str``, *optional*) :
                Unique identifier (int) or username (str) of the target bot.

            name (``str``, *optional*):
                The bot name.

            about (``str``, *optional*):
                The bot bio.

            description (``str``, *optional*):
                Description of the bot;
        """
        peer = None
        if bot:
            peer = await self.resolve_peer(bot)
        r = await self.invoke(
            raw.functions.bots.SetBotInfo(
                lang_code=lang_code,
                bot=peer,
                name=name,
                about=about,
                description=description,
            ),
        )
        return bool(r)
