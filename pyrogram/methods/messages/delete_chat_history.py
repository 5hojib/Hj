from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import pyrogram
from pyrogram import raw, utils

if TYPE_CHECKING:
    from datetime import datetime

log = logging.getLogger(__name__)


class DeleteChatHistory:
    async def delete_chat_history(
        self: pyrogram.Client,
        chat_id: int | str,
        max_id: int = 0,
        revoke: bool | None = None,
        just_clear: bool | None = None,
        min_date: datetime | None = None,
        max_date: datetime | None = None,
    ) -> int:
        """Delete the history of a chat.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
            max_id (``int``, *optional*):
                Maximum ID of message to delete.
            revoke (``bool``, *optional*):
                Deletes messages history for everyone.
                Required ``True`` if using in channel.
            just_clear (``bool``, *optional*):
                If True, clear history for the current user, without actually removing chat.
                For private and simple group chats only.
            min_date (:py:obj:`~datetime.datetime`, *optional*):
                Delete all messages newer than this time.
                For private and simple group chats only.
            max_date (:py:obj:`~datetime.datetime`, *optional*):
                Delete all messages older than this time.
                For private and simple group chats only.

        Returns:
            ``int``: Amount of affected messages

        Example:
            .. code-block:: python

                # Delete all messages in channel
                await app.delete_chat_history(chat_id, revoke=True)
        """
        peer = await self.resolve_peer(chat_id)

        if isinstance(peer, raw.types.InputPeerChannel):
            r = await self.invoke(
                raw.functions.channels.DeleteHistory(
                    channel=raw.types.InputChannel(
                        channel_id=peer.channel_id,
                        access_hash=peer.access_hash,
                    ),
                    max_id=max_id,
                    for_everyone=revoke,
                ),
            )
        else:
            r = await self.invoke(
                raw.functions.messages.DeleteHistory(
                    peer=peer,
                    max_id=max_id,
                    just_clear=just_clear,
                    revoke=revoke,
                    min_date=utils.datetime_to_timestamp(min_date),
                    max_date=utils.datetime_to_timestamp(max_date),
                ),
            )

        return (
            len(r.updates[0].messages)
            if isinstance(peer, raw.types.InputPeerChannel)
            else r.pts_count
        )
