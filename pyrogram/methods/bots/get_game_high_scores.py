from __future__ import annotations

import pyrogram
from pyrogram import raw, types


class GetGameHighScores:
    async def get_game_high_scores(
        self: pyrogram.Client,
        user_id: int | str,
        chat_id: int | str,
        message_id: int | None = None,
    ) -> list[types.GameHighScore]:
        """Get data for high score tables.

        .. include:: /_includes/usable-by/bots.rst

        Parameters:
            user_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).
                You can also use user profile link in form of *t.me/<username>* (str).

            chat_id (``int`` | ``str``, *optional*):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).
                Required if inline_message_id is not specified.

            message_id (``int``, *optional*):
                Identifier of the sent message.
                Required if inline_message_id is not specified.

        Returns:
            List of :obj:`~pyrogram.types.GameHighScore`: On success.

        Example:
            .. code-block:: python

                scores = await app.get_game_high_scores(user_id, chat_id, message_id)
                print(scores)
        """

        r = await self.invoke(
            raw.functions.messages.GetGameHighScores(
                peer=await self.resolve_peer(chat_id),
                id=message_id,
                user_id=await self.resolve_peer(user_id),
            ),
        )

        return types.List(
            types.GameHighScore._parse(self, score, r.users) for score in r.scores
        )
