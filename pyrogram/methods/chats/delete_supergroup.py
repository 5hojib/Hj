from __future__ import annotations

import pyrogram
from pyrogram import raw


class DeleteSupergroup:
    async def delete_supergroup(self: pyrogram.Client, chat_id: int | str) -> bool:
        """Delete a supergroup.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int`` | ``str``):
                The id of the supergroup to be deleted.
                You can also use chat public link in form of *t.me/<username>* (str).

        Returns:
            ``bool``: On success, True is returned.

        Example:
            .. code-block:: python

                await app.delete_supergroup(supergroup_id)
        """
        await self.invoke(
            raw.functions.channels.DeleteChannel(
                channel=await self.resolve_peer(chat_id),
            ),
        )

        return True
