from __future__ import annotations

import pyrogram
from pyrogram import raw, types


class GetAvailableGifts:
    async def get_available_gifts(
        self: pyrogram.Client,
    ) -> list[types.Gift]:
        """Get all gifts that can be sent to other users.

        .. include:: /_includes/usable-by/users.rst

        Returns:
            List of :obj:`~pyrogram.types.Gift`: On success, a list of star gifts is returned.

        Example:
            .. code-block:: python

                app.get_available_gifts()
        """
        r = await self.invoke(raw.functions.payments.GetStarGifts(hash=0))

        return types.List([await types.Gift._parse(self, gift) for gift in r.gifts])
