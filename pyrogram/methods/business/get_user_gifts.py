from __future__ import annotations

from typing import TYPE_CHECKING

import pyrogram
from pyrogram import raw, types

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator


class GetUserGifts:
    async def get_user_gifts(
        self: pyrogram.Client,
        user_id: int | str,
        offset: str = "",
        limit: int = 0,
    ) -> AsyncGenerator[types.UserGift, None] | None:
        """Get gifts saved to profile by the given user.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            user_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target user.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            offset (``str``, *optional*):
                Offset of the first entry to return as received from the previous request; use empty string to get the first chunk of results.

            limit (``int``, *optional*):
                The maximum number of gifts to be returned; must be positive and can't be greater than 100. For optimal performance, the number of returned objects is chosen by Telegram Server and can be smaller than the specified limit.

        Returns:
            ``Generator``: A generator yielding :obj:`~pyrogram.types.UserGift` objects.

        Example:
            .. code-block:: python

                async for user_gift in app.get_user_gifts(user_id):
                    print(user_gift)
        """
        peer = await self.resolve_peer(user_id)

        if not isinstance(peer, raw.types.InputPeerUser | raw.types.InputPeerSelf):
            raise ValueError("user_id must belong to a user.")

        current = 0
        total = abs(limit) or (1 << 31) - 1
        limit = min(100, total)

        while True:
            r = await self.invoke(
                raw.functions.payments.GetUserStarGifts(
                    user_id=peer,
                    offset=offset,
                    limit=limit,
                ),
                sleep_threshold=max(60, self.sleep_threshold),
            )

            users = {u.id: u for u in r.users}

            user_gifts = [
                await types.UserGift._parse(self, gift, users) for gift in r.gifts
            ]

            if not user_gifts:
                return

            for user_gift in user_gifts:
                yield user_gift

                current += 1

                if current >= total:
                    return

            offset = r.next_offset

            if not offset:
                return
