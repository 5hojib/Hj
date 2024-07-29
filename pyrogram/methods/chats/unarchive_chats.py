from __future__ import annotations

import pyrogram
from pyrogram import raw


class UnarchiveChats:
    async def unarchive_chats(
        self: pyrogram.Client,
        chat_ids: int | str | list[int | str],
    ) -> bool:
        """Unarchive one or more chats.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_ids (``int`` | ``str`` | list[``int``, ``str``]):
                Unique identifier (int) or username (str) of the target chat.
                You can also pass a list of ids (int) or usernames (str).
                You can also use chat public link in form of *t.me/<username>* (str).

        Returns:
            ``bool``: On success, True is returned.

        Example:
            .. code-block:: python

                # Unarchive chat
                await app.unarchive_chats(chat_id)

                # Unarchive multiple chats at once
                await app.unarchive_chats([chat_id1, chat_id2, chat_id3])
        """

        if not isinstance(chat_ids, list):
            chat_ids = [chat_ids]

        folder_peers = [
            raw.types.InputFolderPeer(
                peer=await self.resolve_peer(chat), folder_id=0
            )
            for chat in chat_ids
        ]

        await self.invoke(
            raw.functions.folders.EditPeerFolders(
                folder_peers=folder_peers
            )
        )

        return True
