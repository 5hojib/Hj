from __future__ import annotations

import pyrogram
from pyrogram import enums, raw, types, utils


class SendInlineBotResult:
    async def send_inline_bot_result(
        self: pyrogram.Client,
        chat_id: int | str,
        query_id: int,
        result_id: str,
        disable_notification: bool | None = None,
        message_thread_id: int | None = None,
        reply_to_message_id: int | None = None,
        reply_to_story_id: int | None = None,
        quote_text: str | None = None,
        quote_entities: list[types.MessageEntity] | None = None,
        parse_mode: enums.ParseMode | None = None,
    ) -> types.Message:
        """Send an inline bot result.
        Bot results can be retrieved using :meth:`~pyrogram.Client.get_inline_bot_results`

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).
                You can also use user profile/chat public link in form of *t.me/<username>* (str).

            query_id (``int``):
                Unique identifier for the answered query.

            result_id (``str``):
                Unique identifier for the result that was chosen.

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            message_thread_id (``int``, *optional*):
                Unique identifier of a message thread to which the message belongs.
                for supergroups only

            reply_to_message_id (``bool``, *optional*):
                If the message is a reply, ID of the original message.

            quote_text (``str``, *optional*):
                Text to quote.
                for reply_to_message only.

            quote_entities (List of :obj:`~pyrogram.types.MessageEntity`, *optional*):
                List of special entities that appear in quote_text, which can be specified instead of *parse_mode*.
                for reply_to_message only.

            reply_to_story_id (``int``, *optional*):
                If the message is a reply, ID of the target story.

            parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                By default, quote_text are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.
                For quote_text.

        Returns:
            :obj:`~pyrogram.types.Message`: On success, the sent message is returned.

        Example:
            .. code-block:: python

                await app.send_inline_bot_result(chat_id, query_id, result_id)
        """

        reply_to = await utils.get_reply_to(
            client=self,
            chat_id=chat_id,
            reply_to_message_id=reply_to_message_id,
            reply_to_story_id=reply_to_story_id,
            message_thread_id=message_thread_id,
            quote_text=quote_text,
            quote_entities=quote_entities,
            parse_mode=parse_mode,
        )

        r = await self.invoke(
            raw.functions.messages.SendInlineBotResult(
                peer=await self.resolve_peer(chat_id),
                query_id=query_id,
                id=result_id,
                random_id=self.rnd_id(),
                silent=disable_notification or None,
                reply_to=reply_to,
            ),
        )

        for i in r.updates:
            if isinstance(
                i,
                raw.types.UpdateNewMessage | raw.types.UpdateNewChannelMessage,
            ):
                return await types.Message._parse(
                    self,
                    i.message,
                    {i.id: i for i in r.users},
                    {i.id: i for i in r.chats},
                )
        return None
