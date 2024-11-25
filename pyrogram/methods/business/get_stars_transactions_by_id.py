from __future__ import annotations

import pyrogram
from pyrogram import raw, types


class GetStarsTransactionsById:
    async def get_stars_transactions_by_id(
        self: pyrogram.Client,
        transaction_ids: types.InputStarsTransaction
        | list[types.InputStarsTransaction],
        chat_id: int | str = "me",
    ) -> types.StarsStatus:
        """Get stars transactions by transaction id.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            transaction_ids (:obj:`~pyrogram.types.InputStarsTransaction` | List of :obj:`~pyrogram.types.InputStarsTransaction`):
                Pass a single transaction identifier or an iterable of transaction ids (as integers) to get the content of the
                transaction themselves

            chat_id (``int`` | ``str``, *optional*):
                Unique identifier (int) or username (str) of the target user.
                You can also use chat public link in form of *t.me/<username>* (str).
                default to self.
                only for bots.

        Example:
            .. code-block:: python

                # get one transaction by id
                from pyrogram.types import InputStarsTransaction
                app.get_stars_transactions_by_id(InputStarsTransaction(id="transaction_id"))

                # get multiple transactions by id
                from pyrogram.types import InputStarsTransaction
                app.get_stars_transactions_by_id([
                    InputStarsTransaction(id="transaction_id_1"),
                    InputStarsTransaction(id="transaction_id_2")
                ])

                # get one transaction by id from a specific user
                from pyrogram.types import InputStarsTransaction
                app.get_stars_transactions_by_id(InputStarsTransaction(id="transaction_id"), chat_id="username")

                # get multiple transaction by id from a specific user
                from pyrogram.types import InputStarsTransaction
                app.get_stars_transactions_by_id([
                    InputStarsTransaction(id="transaction_id_1"),
                    InputStarsTransaction(id="transaction_id_2")
                ], chat_id="username")

        Returns:
            :obj:`~pyrogram.types.StarsStatus`: On success, a :obj:`~pyrogram.types.StarsStatus` object is returned.
        """
        peer = await self.resolve_peer(chat_id)
        is_iterable = not isinstance(transaction_ids, types.InputStarsTransaction)
        ids = (
            [await transaction_ids.write()]
            if not is_iterable
            else [await x.write() for x in transaction_ids]
        )

        r = await self.invoke(
            raw.functions.payments.GetStarsTransactionsByID(peer=peer, id=ids),
        )
        return types.StarsStatus._parse(self, r)
