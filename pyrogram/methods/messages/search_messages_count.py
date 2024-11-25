from __future__ import annotations

import pyrogram
from pyrogram import enums, raw


class SearchMessagesCount:
    async def search_messages_count(
        self: pyrogram.Client,
        chat_id: int | str,
        query: str = "",
        filter: enums.MessagesFilter = enums.MessagesFilter.EMPTY,
        from_user: int | str | None = None,
        thread_id: int | None = None,
    ) -> int:
        """Get the count of messages resulting from a search inside a chat.

        If you want to get the actual messages, see :meth:`~pyrogram.Client.search_messages`.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).
                You can also use chat public link in form of *t.me/<username>* (str).

            query (``str``, *optional*):
                Text query string.
                Required for text-only messages, optional for media messages (see the ``filter`` argument).
                When passed while searching for media messages, the query will be applied to captions.
                Defaults to "" (empty string).

            filter (:obj:`~pyrogram.enums.MessagesFilter`, *optional*):
                Pass a filter in order to search for specific kind of messages only:

            from_user (``int`` | ``str``, *optional*):
                Unique identifier (int) or username (str) of the target user you want to search for messages from.

            thread_id (``int``, *optional*):
                Unique identifier of the thread (Message.message_thread_id or Message.reply_top_message_id) to search in.

        Returns:
            ``int``: On success, the messages count is returned.
        """
        r = await self.invoke(
            raw.functions.messages.Search(
                peer=await self.resolve_peer(chat_id),
                q=query,
                filter=filter.value(),
                min_date=0,
                max_date=0,
                offset_id=0,
                add_offset=0,
                limit=1,
                min_id=0,
                max_id=0,
                from_id=(await self.resolve_peer(from_user) if from_user else None),
                hash=0,
                top_msg_id=thread_id,
            ),
        )

        if hasattr(r, "count"):
            return r.count
        return len(r.messages)
