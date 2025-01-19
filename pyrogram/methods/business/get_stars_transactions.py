from __future__ import annotations

import pyrogram
from pyrogram import raw, types


class GetStarsTransactions:
    async def get_stars_transactions(
        self: pyrogram.Client,
        chat_id: int | str = "me",
        limit: int = 0,
        offset: str = "",
        is_inbound: bool | None = None,
        is_outbound: bool | None = None,
        is_ascending: bool | None = None,
    ) -> types.StarsStatus:
        """Get stars transactions.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            chat_id (``int`` | ``str``, *optional*):
                Unique identifier (int) or username (str) of the target user.
                You can also use chat public link in form of *t.me/<username>* (str).
                default to self.
                only for bots.

            limit (``int``, *optional*):
                Limits the number of transactions to be retrieved.

            offset (``str``, *optional*):
                Offset the list of transactions to be retrieved.

            is_inbound (``bool``, *optional*):
                True, if only inbound transactions should be retrieved.

            is_outbound (``bool``, *optional*):
                True, if only outbound transactions should be retrieved.

            is_ascending (``bool``, *optional*):
                True, if transactions should be returned in ascending order.

        Example:
            .. code-block:: python

                # get all transactions
                app.get_stars_transactions()

                # get all inbound transactions
                app.get_stars_transactions(is_inbound=True)

                # get all outbound transactions
                app.get_stars_transactions(is_outbound=True)

                # get all transactions in ascending order
                app.get_stars_transactions(is_ascending=True)

        Returns:
            :obj:`~pyrogram.types.StarsStatus`: On success, a :obj:`~pyrogram.types.StarsStatus` object is returned.
        """
        peer = await self.resolve_peer(chat_id)

        r = await self.invoke(
            raw.functions.payments.GetStarsTransactions(
                peer=peer,
                limit=limit,
                offset=offset,
                inbound=is_inbound,
                outbound=is_outbound,
                ascending=is_ascending,
            ),
        )
        return types.StarsStatus._parse(self, r)
