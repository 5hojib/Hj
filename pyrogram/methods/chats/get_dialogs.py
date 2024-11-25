from __future__ import annotations

from typing import TYPE_CHECKING

import pyrogram
from pyrogram import raw, types, utils

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator


class GetDialogs:
    async def get_dialogs(
        self: pyrogram.Client,
        limit: int = 0,
        pinned_only: bool = False,
        chat_list: int = 0,
    ) -> AsyncGenerator[types.Dialog, None] | None:
        """Get a user's dialogs sequentially.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            limit (``int``, *optional*):
                Limits the number of dialogs to be retrieved.
                By default, no limit is applied and all dialogs are returned.

            pinned_only (``bool``, *optional*):
                Pass True if you want to get only pinned dialogs.
                Defaults to False.

            chat_list (``int``, *optional*):
                Chat list from which to get the dialogs; Only Main (0) and Archive (1) chat lists are supported. Defaults to (0) Main chat list.

        Returns:
            ``Generator``: A generator yielding :obj:`~pyrogram.types.Dialog` objects.

        Example:
            .. code-block:: python

                # Iterate through all dialogs
                async for dialog in app.get_dialogs():
                    print(dialog.chat.first_name or dialog.chat.title)
        """
        current = 0
        total = limit or (1 << 31) - 1
        limit = min(100, total)

        offset_date = 0
        offset_id = 0
        offset_peer = raw.types.InputPeerEmpty()

        while True:
            r = await self.invoke(
                raw.functions.messages.GetDialogs(
                    offset_date=offset_date,
                    offset_id=offset_id,
                    offset_peer=offset_peer,
                    limit=limit,
                    hash=0,
                    exclude_pinned=not pinned_only,
                    folder_id=chat_list,
                ),
                sleep_threshold=60,
            )

            users = {i.id: i for i in r.users}
            chats = {i.id: i for i in r.chats}

            messages = {}

            for message in r.messages:
                if isinstance(message, raw.types.MessageEmpty):
                    continue

                chat_id = utils.get_peer_id(message.peer_id)
                messages[chat_id] = await types.Message._parse(
                    self,
                    message,
                    users,
                    chats,
                    replies=1,
                )

            dialogs = []

            for dialog in r.dialogs:
                if not isinstance(dialog, raw.types.Dialog):
                    continue

                dialogs.append(
                    types.Dialog._parse(self, dialog, messages, users, chats),
                )

            if not dialogs:
                return

            last = dialogs[-1]

            offset_id = last.top_message.id
            offset_date = utils.datetime_to_timestamp(last.top_message.date)
            offset_peer = await self.resolve_peer(last.chat.id)

            for dialog in dialogs:
                yield dialog

                current += 1

                if current >= total:
                    return
