from __future__ import annotations

import pyrogram
from pyrogram import raw, types


class GetBusinessConnection:
    async def get_business_connection(
        self: pyrogram.Client,
        business_connection_id: str,
    ) -> types.Message:
        """Use this method to get information about the connection of the bot with a business account.

        .. include:: /_includes/usable-by/bots.rst

        Parameters:
            business_connection_id (``str``):
                Unique identifier of the business connection

        Returns:
            :obj:`~pyrogram.types.BusinessConnection`: On success, the the connection of the bot with a business account is returned.
        """

        r = await self.invoke(
            raw.functions.account.GetBotBusinessConnection(
                connection_id=business_connection_id,
            ),
        )
        for i in r.updates:
            if isinstance(i, (raw.types.UpdateBotBusinessConnect)):
                return await types.BotBusinessConnection._parse(
                    client=self,
                    bot_connection=i.connection,
                )
        return None
