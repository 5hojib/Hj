from __future__ import annotations

import pyrogram
from pyrogram import raw


class GetChatPhotosCount:
    async def get_chat_photos_count(
        self: pyrogram.Client,
        chat_id: int | str,
    ) -> int:
        """Get the total count of photos for a chat.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).
                You can also use user profile/chat public link in form of *t.me/<username>* (str).

        Returns:
            ``int``: On success, the user profile photos count is returned.

        Example:
            .. code-block:: python

                count = await app.get_chat_photos_count("me")
                print(count)
        """

        peer_id = await self.resolve_peer(chat_id)

        if isinstance(peer_id, raw.types.InputPeerChannel):
            r = await self.invoke(
                raw.functions.messages.GetSearchCounters(
                    peer=peer_id,
                    filters=[raw.types.InputMessagesFilterChatPhotos()],
                ),
            )

            return r[0].count
        r = await self.invoke(
            raw.functions.photos.GetUserPhotos(
                user_id=peer_id,
                offset=0,
                max_id=0,
                limit=1,
            ),
        )

        if isinstance(r, raw.types.photos.Photos):
            return len(r.photos)
        return r.count
