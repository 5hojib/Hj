from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import pyrogram
from pyrogram import raw, types, utils
from pyrogram.types.messages_and_media.message import Str

if TYPE_CHECKING:
    from collections.abc import Iterable

log = logging.getLogger(__name__)


class GetMessages:
    async def get_messages(
        self: pyrogram.Client,
        chat_id: int | str | None = None,
        message_ids: int | Iterable[int] | None = None,
        reply_to_message_ids: int | Iterable[int] | None = None,
        replies: int = 1,
        is_scheduled: bool = False,
        link: str | None = None,
    ) -> types.Message | list[types.Message] | types.DraftMessage:
        """Get one or more messages from a chat by using message identifiers.

        You can retrieve up to 200 messages at once.

        .. include:: /_includes/usable-by/users-bots.rst

        You must use exactly one of ``message_ids`` OR (``chat_id``, ``message_ids``) OR (``chat_id``, ``reply_to_message_ids``) OR ``link``.

        Parameters:
            chat_id (``int`` | ``str``, *optional*):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            message_ids (``int`` | Iterable of ``int``, *optional*):
                Pass a single message identifier or an iterable of message ids (as integers) to get the content of the
                message themselves.

            reply_to_message_ids (``int`` | Iterable of ``int``, *optional*):
                Pass a single message identifier or an iterable of message ids (as integers) to get the content of
                the previous message you replied to using this message.
                If *message_ids* is set, this argument will be ignored.

            replies (``int``, *optional*):
                The number of subsequent replies to get for each message.
                Pass 0 for no reply at all or -1 for unlimited replies.
                Defaults to 1.

            is_scheduled (``bool``, *optional*):
                Whether to get scheduled messages. Defaults to False.

            link (``str``, *optional*):
                A link of the message, usually can be copied using ``Copy Link`` functionality OR obtained using :obj:`~pyrogram.raw.types.Message.link` OR  :obj:`~pyrogram.raw.functions.channels.ExportMessageLink`

        Returns:
            :obj:`~pyrogram.types.Message` | List of :obj:`~pyrogram.types.Message` | :obj:`~pyrogram.types.DraftMessage`: In case *message_ids* was not
            a list, a single message is returned, otherwise a list of messages is returned.

        Example:
            .. code-block:: python

                # Get one message
                await app.get_messages(chat_id=chat_id, message_ids=12345)

                # Get more than one message (list of messages)
                await app.get_messages(chat_id=chat_id, message_ids=[12345, 12346])

                # Get message by ignoring any replied-to message
                await app.get_messages(chat_id=chat_id, message_ids=message_id, replies=0)

                # Get message with all chained replied-to messages
                await app.get_messages(chat_id=chat_id, message_ids=message_id, replies=-1)

                # Get the replied-to message of a message
                await app.get_messages(chat_id=chat_id, reply_to_message_ids=message_id)

                # Get message from link
                await app.get_messages(link=link)

        Raises:
            ValueError: In case of invalid arguments.
        """
        if chat_id:
            ids, ids_type = (
                (message_ids, raw.types.InputMessageID)
                if message_ids
                else (reply_to_message_ids, raw.types.InputMessageReplyTo)
                if reply_to_message_ids
                else (None, None)
            )

            if ids is None:
                raise ValueError(
                    "No argument supplied. Either pass message_ids or reply_to_message_ids",
                )

            peer = await self.resolve_peer(chat_id)

            is_iterable = not isinstance(ids, int)
            ids = list(ids) if is_iterable else [ids]

            if replies < 0:
                replies = (1 << 31) - 1

            if is_scheduled:
                rpc = raw.functions.messages.GetScheduledMessages(peer=peer, id=ids)
            else:
                ids = [ids_type(id=i) for i in ids]
                if isinstance(peer, raw.types.InputPeerChannel):
                    rpc = raw.functions.channels.GetMessages(channel=peer, id=ids)
                else:
                    rpc = raw.functions.messages.GetMessages(id=ids)

            r = await self.invoke(rpc, sleep_threshold=-1)

            messages = await utils.parse_messages(self, r, is_scheduled=is_scheduled)

            return messages if is_iterable else messages[0] if messages else None

        if link:
            linkps = link.split("/")
            raw_chat_id, _message_thread_id, message_id = None, None, None
            if len(linkps) == 7 and linkps[3] == "c":
                raw_chat_id = utils.get_channel_id(int(linkps[4]))
                int(linkps[5])
                message_id = int(linkps[6])
            elif len(linkps) == 6:
                if linkps[3] == "c":
                    raw_chat_id = utils.get_channel_id(int(linkps[4]))
                    message_id = int(linkps[5])
                else:
                    raw_chat_id = linkps[3]
                    message_id = int(linkps[5])

            elif not self.me.is_bot and len(linkps) == 5 and linkps[3] == "m":
                r = await self.invoke(
                    raw.functions.account.ResolveBusinessChatLink(slug=linkps[4]),
                )
                users = {i.id: i for i in r.users}
                entities = [
                    types.MessageEntity._parse(self, entity, users)
                    for entity in getattr(r, "entities", [])
                ]
                entities = types.List(filter(lambda x: x is not None, entities))
                chat = None
                cat_id = utils.get_raw_peer_id(r.peer)
                if isinstance(r.peer, raw.types.PeerUser):
                    chat = types.Chat._parse_user_chat(self, users[cat_id])
                return types.DraftMessage(
                    text=Str(r.message).init(entities) or None,
                    entities=entities or None,
                    chat=chat,
                    _raw=r,
                )

            elif len(linkps) == 5:
                raw_chat_id = linkps[3]
                if raw_chat_id == "m":
                    raise ValueError(
                        "Invalid ClientType used to parse this message link",
                    )
                message_id = int(linkps[4])

            return await self.get_messages(
                chat_id=raw_chat_id,
                message_ids=message_id,
            )

        raise ValueError(
            "No argument supplied. Either pass link OR (chat_id, message_ids or reply_to_message_ids)",
        )
