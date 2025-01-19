from __future__ import annotations

import pyrogram
from pyrogram import raw, types


class AnswerWebAppQuery:
    async def answer_web_app_query(
        self: pyrogram.Client,
        web_app_query_id: str,
        result: types.InlineQueryResult,
    ) -> types.SentWebAppMessage:
        """Set the result of an interaction with a `Web App <https://core.telegram.org/bots/webapps>`_ and send a
        corresponding message on behalf of the user to the chat from which the query originated.

        .. include:: /_includes/usable-by/bots.rst

        Parameters:
            web_app_query_id (``str``):
                Unique identifier for the answered query.

            result (:obj:`~pyrogram.types.InlineQueryResult`):
                A list of results for the inline query.

        Returns:
            :obj:`~pyrogram.types.SentWebAppMessage`: On success the sent web app message is returned.
        """

        r = await self.invoke(
            raw.functions.messages.SendWebViewResultMessage(
                bot_query_id=web_app_query_id,
                result=await result.write(self),
            ),
        )

        return types.SentWebAppMessage._parse(r)
