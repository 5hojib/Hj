from __future__ import annotations

import pyrogram
from pyrogram import raw, types


class DeleteBotCommands:
    async def delete_bot_commands(
        self: pyrogram.Client,
        scope: types.BotCommandScope = None,
        language_code: str = "",
    ) -> bool:
        """Delete the list of the bot's commands for the given scope and user language.
        After deletion, higher level commands will be shown to affected users.

        The commands passed will overwrite any command set previously.
        This method can be used by the own bot only.

        .. include:: /_includes/usable-by/bots.rst

        Parameters:
            scope (:obj:`~pyrogram.types.BotCommandScope`, *optional*):
                An object describing the scope of users for which the commands are relevant.
                Defaults to :obj:`~pyrogram.types.BotCommandScopeDefault`.

            language_code (``str``, *optional*):
                A two-letter ISO 639-1 language code.
                If empty, commands will be applied to all users from the given scope, for whose language there are no
                dedicated commands.

        Returns:
            ``bool``: On success, True is returned.

        Example:
            .. code-block:: python

                # Delete commands
                await app.delete_bot_commands()
        """
        if scope is None:
            scope = types.BotCommandScopeDefault()

        return await self.invoke(
            raw.functions.bots.ResetBotCommands(
                scope=await scope.write(self),
                lang_code=language_code,
            ),
        )
