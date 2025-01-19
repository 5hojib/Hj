from __future__ import annotations

import pyrogram
from pyrogram import raw


class DeleteChatPhoto:
    async def delete_chat_photo(self: pyrogram.Client, chat_id: int | str) -> bool:
        """Delete a chat photo.

        You must be an administrator in the chat for this to work and must have the appropriate admin rights.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                You can also use chat public link in form of *t.me/<username>* (str).

        Returns:
            ``bool``: True on success.

        Raises:
            ValueError: if a chat_id belongs to user.

        Example:
            .. code-block:: python

                await app.delete_chat_photo(chat_id)
        """
        peer = await self.resolve_peer(chat_id)

        if isinstance(peer, raw.types.InputPeerChat):
            await self.invoke(
                raw.functions.messages.EditChatPhoto(
                    chat_id=peer.chat_id,
                    photo=raw.types.InputChatPhotoEmpty(),
                ),
            )
        elif isinstance(peer, raw.types.InputPeerChannel):
            await self.invoke(
                raw.functions.channels.EditPhoto(
                    channel=peer,
                    photo=raw.types.InputChatPhotoEmpty(),
                ),
            )
        else:
            raise ValueError(f'The chat_id "{chat_id}" belongs to a user')

        return True
