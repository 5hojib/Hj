from __future__ import annotations

import pyrogram
from pyrogram import raw, types
from pyrogram.types.object import Object


class BotAllowed(Object):
    """Contains information about a allowed bot.

    Parameters:
        attach_menu (``bool``, *optional*):
            True, if the bot can attach to menu.

        from_request (``bool``, *optional*):
            True, if the bot is allowed from request.

        domain (``str``, *optional*):
            The domain of the bot.

        app (:obj:`~pyrogram.types.BotApp`, *optional*):
            The app of the bot.
    """

    def __init__(
        self,
        *,
        attach_menu: bool | None = None,
        from_request: bool | None = None,
        domain: str | None = None,
        app: types.BotApp | None = None,
    ) -> None:
        super().__init__()

        self.attach_menu = attach_menu
        self.from_request = from_request
        self.domain = domain
        self.app = app

    @staticmethod
    def _parse(
        client: pyrogram.Client,
        bot_allowed: raw.types.BotAllowed,
    ) -> BotAllowed:
        bot_app = getattr(bot_allowed, "app", None)
        return BotAllowed(
            attach_menu=getattr(bot_allowed, "attach_menu", None),
            from_request=getattr(bot_allowed, "from_request", None),
            domain=getattr(bot_allowed, "domain", None),
            app=types.BotApp._parse(client, bot_app)
            if bot_app is not None
            else None,
        )
