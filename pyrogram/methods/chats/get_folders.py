from __future__ import annotations

from typing import TYPE_CHECKING

import pyrogram
from pyrogram import raw, types, utils

if TYPE_CHECKING:
    from collections.abc import Iterable


class GetFolders:
    async def get_folders(
        self: pyrogram.Client,
        folder_ids: int | Iterable[int] | None = None,
    ) -> types.Folder | list[types.Folder]:
        """Get one or more folders by using folder identifiers.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            folder_ids (``int`` | Iterable of ``int``, *optional*):
                Pass a single folder identifier or an iterable of folder ids (as integers) to get the content of the
                folders themselves.
                By default all folders are returned.

        Returns:
            :obj:`~pyrogram.types.Folder` | List of :obj:`~pyrogram.types.Folder`: In case *folder_ids* was not
            a list, a single folder is returned, otherwise a list of folders is returned.

        Example:
            .. code-block:: python

                # Get one folder
                await app.get_folders(12345)

                # Get more than one folders (list of folders)
                await app.get_folders([12345, 12346])

                # Get all folders
                await app.get_folders()
        """
        is_iterable = hasattr(folder_ids, "__iter__")
        ids = set(folder_ids) if is_iterable else {folder_ids}

        dialog_filters = await self.invoke(raw.functions.messages.GetDialogFilters())

        raw_folders = [
            folder
            for folder in dialog_filters.filters
            if not isinstance(folder, raw.types.DialogFilterDefault)
            and ((is_iterable and folder.id in ids) or not is_iterable)
        ]

        raw_peers = {}
        for folder in raw_folders:
            for peer in (
                folder.pinned_peers
                + folder.include_peers
                + getattr(folder, "exclude_peers", [])
            ):
                raw_peers[utils.get_peer_id(peer)] = peer

        users = {}
        chats = {}
        for i in range(0, len(raw_peers), 100):
            chunk = list(raw_peers.values())[i : i + 100]
            r = await self.invoke(
                raw.functions.messages.GetPeerDialogs(
                    peers=[raw.types.InputDialogPeer(peer=peer) for peer in chunk],
                ),
            )
            users.update({i.id: i for i in r.users})
            chats.update({i.id: i for i in r.chats})

        folders = types.List(
            types.Folder._parse(self, folder, users, chats) for folder in raw_folders
        )

        if not folders:
            return None

        if folder_ids:
            if is_iterable:
                return folders
            for folder in folders:
                if folder.id == folder_ids:
                    return folder
            return None

        return folders
