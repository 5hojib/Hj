from __future__ import annotations

import pyrogram
from pyrogram import raw


class SetAccountTTL:
    async def set_account_ttl(self: pyrogram.Client, days: int) -> bool:
        """Set days to live of account.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            days (``int``):
                Time to live in days.

        Returns:
            ``bool``: On success, True is returned.

        Example:
            .. code-block:: python

                # Set ttl in days
                await app.set_account_ttl(365)
        """
        return await self.invoke(
            raw.functions.account.SetAccountTTL(
                ttl=raw.types.AccountDaysTTL(days=days),
            ),
        )
