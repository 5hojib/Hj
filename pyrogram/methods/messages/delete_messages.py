from __future__ import annotations

from typing import TYPE_CHECKING

import pyrogram
from pyrogram import raw

if TYPE_CHECKING:
    from collections.abc import Iterable


class DeleteMessages:
    async def delete_messages(
        self: pyrogram.Client,
        chat_id: int | str,
        message_ids: int | Iterable[int],
        revoke: bool = True,
    ) -> int:
        """Delete messages, including service messages.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).
                You can also use chat public link in form of *t.me/<username>* (str).

            message_ids (``int`` | Iterable of ``int``):
                An iterable of message identifiers to delete (integers) or a single message id.

            revoke (``bool``, *optional*):
                Deletes messages on both parts.
                This is only for private cloud chats and normal groups, messages on
                channels and supergroups are always revoked (i.e.: deleted for everyone).
                Defaults to True.

        Returns:
            ``int``: Amount of affected messages

        Example:
            .. code-block:: python

                # Delete one message
                await app.delete_messages(chat_id, message_id)

                # Delete multiple messages at once
                await app.delete_messages(chat_id, list_of_message_ids)

                # Delete messages only on your side (without revoking)
                await app.delete_messages(chat_id, message_id, revoke=False)
        """
        peer = await self.resolve_peer(chat_id)
        message_ids = (
            list(message_ids) if not isinstance(message_ids, int) else [message_ids]
        )

        if isinstance(peer, raw.types.InputPeerChannel):
            r = await self.invoke(
                raw.functions.channels.DeleteMessages(channel=peer, id=message_ids),
            )
        else:
            r = await self.invoke(
                raw.functions.messages.DeleteMessages(id=message_ids, revoke=revoke),
            )

        return r.pts_count
