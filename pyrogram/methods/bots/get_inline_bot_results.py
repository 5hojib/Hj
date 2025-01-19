from __future__ import annotations

import pyrogram
from pyrogram import raw
from pyrogram.errors import UnknownError


class GetInlineBotResults:
    async def get_inline_bot_results(
        self: pyrogram.Client,
        bot: int | str,
        query: str = "",
        offset: str = "",
        latitude: float | None = None,
        longitude: float | None = None,
    ):
        """Get bot results via inline queries.
        You can then send a result using :meth:`~pyrogram.Client.send_inline_bot_result`

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            bot (``int`` | ``str``):
                Unique identifier of the inline bot you want to get results from. You can specify
                a @username (str) or a bot ID (int).
                You can also use bot profile link in form of *t.me/<username>* (str).

            query (``str``, *optional*):
                Text of the query (up to 512 characters).
                Defaults to "" (empty string).

            offset (``str``, *optional*):
                Offset of the results to be returned.

            latitude (``float``, *optional*):
                Latitude of the location.
                Useful for location-based results only.

            longitude (``float``, *optional*):
                Longitude of the location.
                Useful for location-based results only.

        Returns:
            :obj:`BotResults <pyrogram.api.types.messages.BotResults>`: On Success.

        Raises:
            TimeoutError: In case the bot fails to answer within 10 seconds.

        Example:
            .. code-block:: python

                results = await app.get_inline_bot_results("pyrogrambot")
                print(results)
        """

        try:
            return await self.invoke(
                raw.functions.messages.GetInlineBotResults(
                    bot=await self.resolve_peer(bot),
                    peer=raw.types.InputPeerSelf(),
                    query=query,
                    offset=offset,
                    geo_point=raw.types.InputGeoPoint(lat=latitude, long=longitude)
                    if (latitude is not None and longitude is not None)
                    else None,
                ),
            )
        except UnknownError as e:
            if e.value.error_code == -503 and e.value.error_message == "Timeout":
                raise TimeoutError("The inline bot didn't answer in time") from None
            raise e
