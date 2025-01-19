from __future__ import annotations

import re
from pathlib import Path
from typing import TYPE_CHECKING

import pyrogram
from pyrogram import enums, raw, types, utils
from pyrogram.file_id import FileType

from .inline_session import get_session

if TYPE_CHECKING:
    from datetime import datetime


class SendPaidMedia:
    async def send_paid_media(
        self: pyrogram.Client,
        chat_id: int | str,
        star_count: int,
        media: list[types.InputPaidMediaPhoto | types.InputPaidMediaVideo],
        caption: str = "",
        parse_mode: enums.ParseMode | None = None,
        caption_entities: list[types.MessageEntity] | None = None,
        show_caption_above_media: bool | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        business_connection_id: str | None = None,
        schedule_date: datetime | None = None,
    ) -> types.Message:
        """Use this method to send paid media.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier for the target chat or username of the target channel (in the format @channelusername).

            star_count (``int``):
                The number of Telegram Stars that must be paid to buy access to the media.

            media (List of :obj:`~pyrogram.types.InputPaidMedia`):
                A list describing the media to be sent; up to 10 items.

            caption (``str``, *optional*):
                Media caption, 0-1024 characters after entities parsing.

            parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                By default, texts are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.

            caption_entities (List of :obj:`~pyrogram.types.MessageEntity`):
                List of special entities that appear in the caption, which can be specified instead of *parse_mode*.

            show_caption_above_media (``bool``, *optional*):
                Pass True, if the caption must be shown above the message media.

            disable_notification (``bool``, *optional*):
                Sends the message silently. Users will receive a notification with no sound.

            protect_content (``bool``, *optional*):
                Pass True if the content of the message must be protected from forwarding and saving; for bots only.

            business_connection_id (``str``, *optional*):
                Unique identifier of the business connection on behalf of which the message will be sent.

            schedule_date (:obj:`~datetime.datetime`, *optional*):
                Date when the message will be automatically sent. Pass a :obj:`~datetime.datetime` object.

        Returns:
            :obj:`~pyrogram.types.Message`: On success, the sent message is returned.

        """
        multi_media = []

        await self.resolve_peer(chat_id)
        for i in media:
            if isinstance(i, types.InputPaidMediaPhoto):
                if isinstance(i.media, str):
                    if Path(i.media).is_file():
                        media = await self.invoke(
                            raw.functions.messages.UploadMedia(
                                peer=await self.resolve_peer(chat_id),
                                media=raw.types.InputMediaUploadedPhoto(
                                    file=await self.save_file(i.media),
                                ),
                            ),
                        )

                        media = raw.types.InputMediaPhoto(
                            id=raw.types.InputPhoto(
                                id=media.photo.id,
                                access_hash=media.photo.access_hash,
                                file_reference=media.photo.file_reference,
                            ),
                        )
                    elif re.match("^https?://", i.media):
                        media = await self.invoke(
                            raw.functions.messages.UploadMedia(
                                peer=await self.resolve_peer(chat_id),
                                media=raw.types.InputMediaPhotoExternal(url=i.media),
                            ),
                        )

                        media = raw.types.InputMediaPhoto(
                            id=raw.types.InputPhoto(
                                id=media.photo.id,
                                access_hash=media.photo.access_hash,
                                file_reference=media.photo.file_reference,
                            ),
                        )
                    else:
                        media = utils.get_input_media_from_file_id(
                            i.media,
                            FileType.PHOTO,
                        )
                else:
                    media = await self.invoke(
                        raw.functions.messages.UploadMedia(
                            peer=await self.resolve_peer(chat_id),
                            media=raw.types.InputMediaUploadedPhoto(
                                file=await self.save_file(i.media),
                            ),
                        ),
                    )

                    media = raw.types.InputMediaPhoto(
                        id=raw.types.InputPhoto(
                            id=media.photo.id,
                            access_hash=media.photo.access_hash,
                            file_reference=media.photo.file_reference,
                        ),
                    )
            elif isinstance(i, types.InputPaidMediaVideo):
                if isinstance(i.media, str):
                    if Path(i.media).is_file():
                        attributes = [
                            raw.types.DocumentAttributeVideo(
                                supports_streaming=i.supports_streaming or None,
                                duration=i.duration,
                                w=i.width,
                                h=i.height,
                            ),
                            raw.types.DocumentAttributeFilename(
                                file_name=Path(i.media).name,
                            ),
                        ]
                        media = await self.invoke(
                            raw.functions.messages.UploadMedia(
                                peer=await self.resolve_peer(chat_id),
                                media=raw.types.InputMediaUploadedDocument(
                                    file=await self.save_file(i.media),
                                    thumb=await self.save_file(i.thumbnail),
                                    mime_type=self.guess_mime_type(i.media)
                                    or "video/mp4",
                                    nosound_video=True,
                                    attributes=attributes,
                                ),
                            ),
                        )

                        media = raw.types.InputMediaDocument(
                            id=raw.types.InputDocument(
                                id=media.document.id,
                                access_hash=media.document.access_hash,
                                file_reference=media.document.file_reference,
                            ),
                        )
                    elif re.match("^https?://", i.media):
                        media = await self.invoke(
                            raw.functions.messages.UploadMedia(
                                peer=await self.resolve_peer(chat_id),
                                media=raw.types.InputMediaDocumentExternal(
                                    url=i.media,
                                ),
                            ),
                        )

                        media = raw.types.InputMediaDocument(
                            id=raw.types.InputDocument(
                                id=media.document.id,
                                access_hash=media.document.access_hash,
                                file_reference=media.document.file_reference,
                            ),
                        )
                    else:
                        media = utils.get_input_media_from_file_id(
                            i.media,
                            FileType.VIDEO,
                        )
                else:
                    media = await self.invoke(
                        raw.functions.messages.UploadMedia(
                            peer=await self.resolve_peer(chat_id),
                            media=raw.types.InputMediaUploadedDocument(
                                file=await self.save_file(i.media),
                                thumb=await self.save_file(i.thumbnail),
                                mime_type=self.guess_mime_type(
                                    getattr(i.media, "name", "video.mp4"),
                                )
                                or "video/mp4",
                                attributes=[
                                    raw.types.DocumentAttributeVideo(
                                        supports_streaming=i.supports_streaming
                                        or None,
                                        duration=i.duration,
                                        w=i.width,
                                        h=i.height,
                                    ),
                                    raw.types.DocumentAttributeFilename(
                                        file_name=getattr(
                                            i.media,
                                            "name",
                                            "video.mp4",
                                        ),
                                    ),
                                ],
                            ),
                        ),
                    )

                    media = raw.types.InputMediaDocument(
                        id=raw.types.InputDocument(
                            id=media.document.id,
                            access_hash=media.document.access_hash,
                            file_reference=media.document.file_reference,
                        ),
                    )
            else:
                raise ValueError(
                    f"{i.__class__.__name__} is not a supported type for send_paid_media",
                )
            multi_media.append(media)

        rpc = raw.functions.messages.SendMedia(
            peer=await self.resolve_peer(chat_id),
            media=raw.types.InputMediaPaidMedia(
                stars_amount=star_count,
                extended_media=multi_media,
            ),
            silent=disable_notification or None,
            random_id=self.rnd_id(),
            schedule_date=utils.datetime_to_timestamp(schedule_date),
            noforwards=protect_content,
            invert_media=show_caption_above_media,
            **await utils.parse_text_entities(
                self,
                caption,
                parse_mode,
                caption_entities,
            ),
        )
        session = None
        business_connection = None
        if business_connection_id:
            business_connection = self.business_user_connection_cache[
                business_connection_id
            ]
            if not business_connection:
                business_connection = await self.get_business_connection(
                    business_connection_id,
                )
            session = await get_session(
                self,
                business_connection._raw.connection.dc_id,
            )
        if business_connection_id:
            r = await session.invoke(
                raw.functions.InvokeWithBusinessConnection(
                    query=rpc,
                    connection_id=business_connection_id,
                ),
            )
            # await session.stop()
        else:
            r = await self.invoke(rpc, sleep_threshold=60)
        for i in r.updates:
            if isinstance(
                i,
                raw.types.UpdateNewMessage
                | raw.types.UpdateNewChannelMessage
                | raw.types.UpdateNewScheduledMessage,
            ):
                return await types.Message._parse(
                    self,
                    i.message,
                    {i.id: i for i in r.users},
                    {i.id: i for i in r.chats},
                    is_scheduled=isinstance(i, raw.types.UpdateNewScheduledMessage),
                    replies=1,
                )
            if isinstance(i, (raw.types.UpdateBotNewBusinessMessage)):
                return await types.Message._parse(
                    self,
                    i.message,
                    {i.id: i for i in r.users},
                    {i.id: i for i in r.chats},
                    business_connection_id=getattr(
                        i,
                        "connection_id",
                        business_connection_id,
                    ),
                    raw_reply_to_message=i.reply_to_message,
                    replies=0,
                )
        return None
