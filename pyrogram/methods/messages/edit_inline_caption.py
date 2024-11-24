from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pyrogram
    from pyrogram import enums, types


class EditInlineCaption:
    async def edit_inline_caption(
        self: pyrogram.Client,
        inline_message_id: str,
        caption: str,
        parse_mode: enums.ParseMode | None = None,
        reply_markup: types.InlineKeyboardMarkup = None,
        invert_media: bool | None = None,
    ) -> bool:
        """Edit the caption of inline media messages.

        .. include:: /_includes/usable-by/bots.rst

        Parameters:
            inline_message_id (``str``):
                Identifier of the inline message.

            caption (``str``):
                New caption of the media message.

            parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                By default, texts are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.

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
                await app.edit_inline_caption(inline_message_id, "new media caption")
        """
        return await self.edit_inline_text(
            inline_message_id=inline_message_id,
            text=caption,
            parse_mode=parse_mode,
            reply_markup=reply_markup,
            invert_media=invert_media,
        )
