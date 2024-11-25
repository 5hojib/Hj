from __future__ import annotations

import pyrogram
from pyrogram import raw, types


class CreateSupergroup:
    async def create_supergroup(
        self: pyrogram.Client,
        title: str,
        description: str = "",
    ) -> types.Chat:
        """Create a new supergroup.

        .. note::

            If you want to create a new basic group, use :meth:`~pyrogram.Client.create_group` instead.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            title (``str``):
                The supergroup title.

            description (``str``, *optional*):
                The supergroup description.

        Returns:
            :obj:`~pyrogram.types.Chat`: On success, a chat object is returned.

        Example:
            .. code-block:: python

                await app.create_supergroup("Supergroup Title", "Supergroup Description")
        """
        r = await self.invoke(
            raw.functions.channels.CreateChannel(
                title=title,
                about=description,
                megagroup=True,
            ),
        )

        return types.Chat._parse_chat(self, r.chats[0])
