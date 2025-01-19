from __future__ import annotations

import pyrogram
from pyrogram import enums, raw, types


class GetPrivacy:
    async def get_privacy(
        self: pyrogram.Client,
        key: enums.PrivacyKey,
    ) -> types.PrivacyRule:
        """Get account privacy rules.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            key (:obj:`~pyrogram.enums.PrivacyKey`):
                Privacy key.

        Returns:
            List of :obj:`~pyrogram.types.PrivacyRule`: On success, the list of privacy rules is returned.

        Example:
            .. code-block:: python

                from pyrogram import enums
                await app.get_privacy(enums.PrivacyKey.PHONE_NUMBER)
        """
        r = await self.invoke(raw.functions.account.GetPrivacy(key=key.value()))

        users = {i.id: i for i in r.users}
        chats = {i.id: i for i in r.chats}

        return types.List(
            types.PrivacyRule._parse(self, rule, users, chats) for rule in r.rules
        )
