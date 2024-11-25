from __future__ import annotations

import pyrogram
from pyrogram import raw


class GetContactsCount:
    async def get_contacts_count(self: pyrogram.Client) -> int:
        """Get the total count of contacts from your Telegram address book.

        .. include:: /_includes/usable-by/users.rst

        Returns:
            ``int``: On success, the contacts count is returned.

        Example:
            .. code-block:: python

                count = await app.get_contacts_count()
                print(count)
        """

        return len(
            (await self.invoke(raw.functions.contacts.GetContacts(hash=0))).contacts,
        )
