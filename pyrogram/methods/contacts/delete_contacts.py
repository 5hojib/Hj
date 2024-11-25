from __future__ import annotations

import pyrogram
from pyrogram import raw, types


class DeleteContacts:
    async def delete_contacts(
        self: pyrogram.Client,
        user_ids: int | str | list[int | str],
    ) -> types.User | list[types.User] | None:
        """Delete contacts from your Telegram address book.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            user_ids (``int`` | ``str`` | List of ``int`` or ``str``):
                A single user id/username or a list of user identifiers (id or username).
                You can also use user profile link in form of *t.me/<username>* (str).

        Returns:
            :obj:`~pyrogram.types.User` | List of :obj:`~pyrogram.types.User` | ``None``: In case *user_ids* was an
            integer or a string, a single User object is returned. In case *user_ids* was a list, a list of User objects
            is returned. In case nothing changed after calling the method (for example, when deleting a non-existent
            contact), None is returned.

        Example:
            .. code-block:: python

                await app.delete_contacts(user_id)
                await app.delete_contacts([user_id1, user_id2, user_id3])
        """
        is_list = isinstance(user_ids, list)

        if not is_list:
            user_ids = [user_ids]

        r = await self.invoke(
            raw.functions.contacts.DeleteContacts(
                id=[await self.resolve_peer(i) for i in user_ids],
            ),
        )

        if not r.updates:
            return None

        users = types.List([types.User._parse(self, i) for i in r.users])

        return users if is_list else users[0]
