from __future__ import annotations

import pyrogram
from pyrogram import raw


class GetDialogsCount:
    async def get_dialogs_count(
        self: pyrogram.Client,
        pinned_only: bool = False,
        chat_list: int = 0,
    ) -> int:
        """Get the total count of your dialogs.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            pinned_only (``bool``, *optional*):
                Pass True if you want to count only pinned dialogs.
                Defaults to False.

            chat_list (``int``, *optional*):
                Chat list from which to get the dialogs; Only Main (0) and Archive (1) chat lists are supported. Defaults to (0) Main chat list.

        Returns:
            ``int``: On success, the dialogs count is returned.

        Example:
            .. code-block:: python

                count = await app.get_dialogs_count()
                print(count)
        """

        if pinned_only:
            return len(
                (
                    await self.invoke(
                        raw.functions.messages.GetPinnedDialogs(folder_id=chat_list),
                    )
                ).dialogs,
            )
        r = await self.invoke(
            raw.functions.messages.GetDialogs(
                offset_date=0,
                offset_id=0,
                offset_peer=raw.types.InputPeerEmpty(),
                limit=1,
                hash=0,
                folder_id=chat_list,
            ),
        )

        if isinstance(r, raw.types.messages.Dialogs):
            return len(r.dialogs)
        return r.count
