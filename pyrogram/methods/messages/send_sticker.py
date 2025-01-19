from __future__ import annotations

import re
from pathlib import Path
from typing import TYPE_CHECKING, BinaryIO

import pyrogram
from pyrogram import StopTransmissionError, enums, raw, types, utils
from pyrogram.errors import FilePartMissing
from pyrogram.file_id import FileType

if TYPE_CHECKING:
    from collections.abc import Callable
    from datetime import datetime


class SendSticker:
    async def send_sticker(
        self: pyrogram.Client,
        chat_id: int | str,
        sticker: str | BinaryIO,
        emoji: str | None = None,
        disable_notification: bool | None = None,
        message_thread_id: int | None = None,
        business_connection_id: str | None = None,
        reply_to_message_id: int | None = None,
        reply_to_story_id: int | None = None,
        reply_to_chat_id: int | str | None = None,
        quote_text: str | None = None,
        quote_entities: list[types.MessageEntity] | None = None,
        parse_mode: enums.ParseMode | None = None,
        schedule_date: datetime | None = None,
        protect_content: bool | None = None,
        allow_paid_broadcast: bool | None = None,
        message_effect_id: int | None = None,
        reply_markup: types.InlineKeyboardMarkup
        | types.ReplyKeyboardMarkup
        | types.ReplyKeyboardRemove
        | types.ForceReply = None,
        progress: Callable | None = None,
        progress_args: tuple = (),
    ) -> types.Message | None:
        """Send static .webp or animated .tgs stickers.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).
                You can also use chat public link in form of *t.me/<username>* (str).

            sticker (``str`` | ``BinaryIO``):
                Sticker to send.
                Pass a file_id as string to send a sticker that exists on the Telegram servers,
                pass an HTTP URL as a string for Telegram to get a .webp sticker file from the Internet,
                pass a file path as string to upload a new sticker that exists on your local machine, or
                pass a binary file-like object with its attribute ".name" set for in-memory uploads.

            emoji (``str``, *optional*):
                Emoji associated with the sticker; only for just uploaded stickers

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            message_thread_id (``int``, *optional*):
                Unique identifier for the target message thread (topic) of the forum.
                for forum supergroups only.

            business_connection_id (``str``, *optional*):
                Business connection identifier.
                for business bots only.

            reply_to_message_id (``int``, *optional*):
                If the message is a reply, ID of the original message.

            reply_to_story_id (``int``, *optional*):
                If the message is a reply, ID of the target story.

            reply_to_chat_id (``int`` | ``str``, *optional*):
                Unique identifier for the origin chat.
                for reply to message from another chat.
                You can also use chat public link in form of *t.me/<username>* (str).

            quote_text (``str``, *optional*):
                Text to quote.
                for reply_to_message only.

            quote_entities (List of :obj:`~pyrogram.types.MessageEntity`, *optional*):
                List of special entities that appear in quote_text, which can be specified instead of *parse_mode*.
                for reply_to_message only.

            parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                By default, quote_text are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.
                For quote_text.

            schedule_date (:py:obj:`~datetime.datetime`, *optional*):
                Date when the message will be automatically sent.

            protect_content (``bool``, *optional*):
                Protects the contents of the sent message from forwarding and saving.

            allow_paid_broadcast (``bool``, *optional*):
                Pass True to allow the message to ignore regular broadcast limits for a small fee; for bots only

            message_effect_id (``int`` ``64-bit``, *optional*):
                Unique identifier of the message effect to be added to the message; for private chats only.

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardRemove` | :obj:`~pyrogram.types.ForceReply`, *optional*):
                Additional interface options. An object for an inline keyboard, custom reply keyboard,
                instructions to remove reply keyboard or to force a reply from the user.

            progress (``Callable``, *optional*):
                Pass a callback function to view the file transmission progress.
                The function must take *(current, total)* as positional arguments (look at Other Parameters below for a
                detailed description) and will be called back each time a new file chunk has been successfully
                transmitted.

            progress_args (``tuple``, *optional*):
                Extra custom arguments for the progress callback function.
                You can pass anything you need to be available in the progress callback scope; for example, a Message
                object or a Client instance in order to edit the message with the updated progress status.

        Other Parameters:
            current (``int``):
                The amount of bytes transmitted so far.

            total (``int``):
                The total size of the file.

            *args (``tuple``, *optional*):
                Extra custom arguments as defined in the ``progress_args`` parameter.
                You can either keep ``*args`` or add every single extra argument in your function signature.

        Returns:
            :obj:`~pyrogram.types.Message` | ``None``: On success, the sent sticker message is returned, otherwise,
            in case the upload is deliberately stopped with :meth:`~pyrogram.Client.stop_transmission`, None is
            returned.

        Example:
            .. code-block:: python

                # Send sticker by uploading from local file
                await app.send_sticker("me", "sticker.webp")

                # Send sticker using file_id
                await app.send_sticker("me", file_id)
        """
        file = None

        reply_to = await utils.get_reply_to(
            client=self,
            chat_id=chat_id,
            reply_to_message_id=reply_to_message_id,
            reply_to_story_id=reply_to_story_id,
            message_thread_id=message_thread_id,
            reply_to_chat_id=reply_to_chat_id,
            quote_text=quote_text,
            quote_entities=quote_entities,
            parse_mode=parse_mode,
        )

        try:
            if isinstance(sticker, str):
                if Path(sticker).is_file():
                    file = await self.save_file(
                        sticker,
                        progress=progress,
                        progress_args=progress_args,
                    )
                    media = raw.types.InputMediaUploadedDocument(
                        mime_type=self.guess_mime_type(sticker) or "image/webp",
                        file=file,
                        attributes=[
                            raw.types.DocumentAttributeFilename(
                                file_name=Path(sticker).name,
                            ),
                            raw.types.DocumentAttributeSticker(
                                alt=emoji,
                                stickerset=raw.types.InputStickerSetEmpty(),
                            ),
                        ],
                    )
                elif re.match("^https?://", sticker):
                    media = raw.types.InputMediaDocumentExternal(url=sticker)
                else:
                    media = utils.get_input_media_from_file_id(
                        sticker,
                        FileType.STICKER,
                    )
            else:
                file = await self.save_file(
                    sticker,
                    progress=progress,
                    progress_args=progress_args,
                )
                media = raw.types.InputMediaUploadedDocument(
                    mime_type=self.guess_mime_type(sticker.name) or "image/webp",
                    file=file,
                    attributes=[
                        raw.types.DocumentAttributeFilename(file_name=sticker.name),
                    ],
                )

            while True:
                try:
                    rpc = raw.functions.messages.SendMedia(
                        peer=await self.resolve_peer(chat_id),
                        media=media,
                        silent=disable_notification or None,
                        reply_to=reply_to,
                        random_id=self.rnd_id(),
                        schedule_date=utils.datetime_to_timestamp(schedule_date),
                        noforwards=protect_content,
                        allow_paid_floodskip=allow_paid_broadcast,
                        effect=message_effect_id,
                        reply_markup=await reply_markup.write(self)
                        if reply_markup
                        else None,
                        message="",
                    )
                    if business_connection_id is not None:
                        r = await self.invoke(
                            raw.functions.InvokeWithBusinessConnection(
                                connection_id=business_connection_id,
                                query=rpc,
                            ),
                        )
                    else:
                        r = await self.invoke(rpc)
                except FilePartMissing as e:
                    await self.save_file(sticker, file_id=file.id, file_part=e.value)
                else:
                    for i in r.updates:
                        if isinstance(
                            i,
                            raw.types.UpdateNewMessage
                            | raw.types.UpdateNewChannelMessage
                            | raw.types.UpdateNewScheduledMessage
                            | raw.types.UpdateBotNewBusinessMessage,
                        ):
                            return await types.Message._parse(
                                self,
                                i.message,
                                {i.id: i for i in r.users},
                                {i.id: i for i in r.chats},
                                is_scheduled=isinstance(
                                    i,
                                    raw.types.UpdateNewScheduledMessage,
                                ),
                                business_connection_id=business_connection_id,
                            )
        except StopTransmissionError:
            return None
