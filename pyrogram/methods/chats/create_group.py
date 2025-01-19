from __future__ import annotations

import pyrogram
from pyrogram import raw, types


class CreateGroup:
    async def create_group(
        self: pyrogram.Client,
        title: str,
        users: int | str | list[int | str],
    ) -> types.Chat:
        """Create a new basic group.

        .. note::

            If you want to create a new supergroup, use :meth:`~pyrogram.Client.create_supergroup` instead.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            title (``str``):
                The group title.

            users (``int`` | ``str`` | List of ``int`` or ``str``):
                Users to create a chat with.
                You must pass at least one user using their IDs (int), usernames (str) or phone numbers (str).
                Multiple users can be invited by passing a list of IDs, usernames or phone numbers.

        Returns:
            :obj:`~pyrogram.types.Chat`: On success, a chat object is returned.

        Example:
            .. code-block:: python

                await app.create_group("Group Title", user_id)
        """
        if not isinstance(users, list):
            users = [users]

        r = await self.invoke(
            raw.functions.messages.CreateChat(
                title=title,
                users=[await self.resolve_peer(u) for u in users],
            ),
        )

        return types.Chat._parse_chat(self, r.chats[0])
