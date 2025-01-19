from __future__ import annotations

import pyrogram
from pyrogram import enums, raw, types, utils

from .inline_session import get_session


class EditInlineText:
    async def edit_inline_text(
        self: pyrogram.Client,
        inline_message_id: str,
        text: str,
        parse_mode: enums.ParseMode | None = None,
        disable_web_page_preview: bool | None = None,
        reply_markup: types.InlineKeyboardMarkup = None,
        invert_media: bool | None = None,
    ) -> bool:
        """Edit the text of inline messages.

        .. include:: /_includes/usable-by/bots.rst

        Parameters:
            inline_message_id (``str``):
                Identifier of the inline message.

            text (``str``):
                New text of the message.

            parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                By default, texts are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.

            disable_web_page_preview (``bool``, *optional*):
                Disables link previews for links in this message.

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup`, *optional*):
                An InlineKeyboardMarkup object.

            invert_media (``bool``, *optional*):
                True, If the media position is inverted.
                only animation, photo, video, and webpage preview messages.

        Returns:
            ``bool``: On success, True is returned.

        Example:
            .. code-block:: python

                # Bots only

                # Simple edit text
                await app.edit_inline_text(inline_message_id, "new text")

                # Take the same text message, remove the web page preview only
                await app.edit_inline_text(
                    inline_message_id, message.text,
                    disable_web_page_preview=True)
        """

        unpacked = utils.unpack_inline_message_id(inline_message_id)
        dc_id = unpacked.dc_id

        session = await get_session(self, dc_id)

        return await session.invoke(
            raw.functions.messages.EditInlineBotMessage(
                id=unpacked,
                no_webpage=disable_web_page_preview or None,
                reply_markup=await reply_markup.write(self)
                if reply_markup
                else None,
                **await self.parser.parse(text, parse_mode),
                invert_media=invert_media,
            ),
            sleep_threshold=self.sleep_threshold,
        )
