from __future__ import annotations

import pyrogram
from pyrogram import raw, types


class AddContact:
    async def add_contact(
        self: pyrogram.Client,
        user_id: int | str,
        first_name: str,
        last_name: str = "",
        phone_number: str = "",
        share_phone_number: bool = False,
    ):
        """Add an existing Telegram user as contact, even without a phone number.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            user_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target user.
                You can also use user profile link in form of *t.me/<username>* (str).

            first_name (``str``):
                User's first name.

            last_name (``str``, *optional*):
                User's last name.

            phone_number (``str``, *optional*):
                User's phone number.

            share_phone_number (``bool``, *optional*):
                Whether or not to share the phone number with the user.
                Defaults to False.

        Returns:
            :obj:`~pyrogram.types.User`: On success the user is returned.

        Example:
            .. code-block:: python

                # Add contact by id
                await app.add_contact(12345678, "Foo")

                # Add contact by username
                await app.add_contact("username", "Bar")
        """
        r = await self.invoke(
            raw.functions.contacts.AddContact(
                id=await self.resolve_peer(user_id),
                first_name=first_name,
                last_name=last_name,
                phone=phone_number,
                add_phone_privacy_exception=share_phone_number,
            ),
        )

        return types.User._parse(self, r.users[0])
