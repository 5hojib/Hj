from __future__ import annotations

import pyrogram
from pyrogram import enums, raw, types, utils


class TranslateText:
    async def translate_message_text(
        self: pyrogram.Client,
        to_language_code: str,
        chat_id: int | str,
        message_ids: int | list[int],
    ) -> types.TranslatedText | list[types.TranslatedText]:
        """Extracts text or caption of the given message and translates it to the given language. If the current user is a Telegram Premium user, then text formatting is preserved.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            to_language_code (``str``):
                Language code of the language to which the message is translated.
                Must be one of "af", "sq", "am", "ar", "hy", "az", "eu", "be", "bn", "bs", "bg", "ca", "ceb", "zh-CN", "zh", "zh-Hans", "zh-TW", "zh-Hant", "co", "hr", "cs", "da", "nl", "en", "eo", "et", "fi", "fr", "fy", "gl", "ka", "de", "el", "gu", "ht", "ha", "haw", "he", "iw", "hi", "hmn", "hu", "is", "ig", "id", "in", "ga", "it", "ja", "jv", "kn", "kk", "km", "rw", "ko", "ku", "ky", "lo", "la", "lv", "lt", "lb", "mk", "mg", "ms", "ml", "mt", "mi", "mr", "mn", "my", "ne", "no", "ny", "or", "ps", "fa", "pl", "pt", "pa", "ro", "ru", "sm", "gd", "sr", "st", "sn", "sd", "si", "sk", "sl", "so", "es", "su", "sw", "sv", "tl", "tg", "ta", "tt", "te", "th", "tr", "tk", "uk", "ur", "ug", "uz", "vi", "cy", "xh", "yi", "ji", "yo", "zu".

            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            message_ids (``int`` | List of ``int``):
                Identifier or list of message identifiers of the target message.

        Returns:
            :obj:`~pyrogram.types.TranslatedText` | List of :obj:`~pyrogram.types.TranslatedText`: In case *message_ids* was not
            a list, a single result is returned, otherwise a list of results is returned.

        Example:
            .. code-block:: python

                await app.translate_message_text("en", chat_id, message_id)
        """
        ids = [message_ids] if not isinstance(message_ids, list) else message_ids

        r = await self.invoke(
            raw.functions.messages.TranslateText(
                to_lang=to_language_code,
                peer=await self.resolve_peer(chat_id),
                id=ids,
            ),
        )

        return (
            types.TranslatedText._parse(self, r.result[0])
            if len(r.result) == 1
            else [types.TranslatedText._parse(self, i) for i in r.result]
        )

    async def translate_text(
        self: pyrogram.Client,
        to_language_code: str,
        text: str,
        parse_mode: enums.ParseMode | None = None,
        entities: list[types.MessageEntity] | None = None,
    ) -> types.TranslatedText | list[types.TranslatedText]:
        """Translates a text to the given language. If the current user is a Telegram Premium user, then text formatting is preserved.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            to_language_code (``str``):
                Language code of the language to which the message is translated.
                Must be one of "af", "sq", "am", "ar", "hy", "az", "eu", "be", "bn", "bs", "bg", "ca", "ceb", "zh-CN", "zh", "zh-Hans", "zh-TW", "zh-Hant", "co", "hr", "cs", "da", "nl", "en", "eo", "et", "fi", "fr", "fy", "gl", "ka", "de", "el", "gu", "ht", "ha", "haw", "he", "iw", "hi", "hmn", "hu", "is", "ig", "id", "in", "ga", "it", "ja", "jv", "kn", "kk", "km", "rw", "ko", "ku", "ky", "lo", "la", "lv", "lt", "lb", "mk", "mg", "ms", "ml", "mt", "mi", "mr", "mn", "my", "ne", "no", "ny", "or", "ps", "fa", "pl", "pt", "pa", "ro", "ru", "sm", "gd", "sr", "st", "sn", "sd", "si", "sk", "sl", "so", "es", "su", "sw", "sv", "tl", "tg", "ta", "tt", "te", "th", "tr", "tk", "uk", "ur", "ug", "uz", "vi", "cy", "xh", "yi", "ji", "yo", "zu".

            text (``str``):
                Text to translate.

            parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                By default, texts are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.

            entities (List of :obj:`~pyrogram.types.MessageEntity`):
                List of special entities that appear in message text, which can be specified instead of *parse_mode*.

        Returns:
            :obj:`~pyrogram.types.TranslatedText` | List of :obj:`~pyrogram.types.TranslatedText`: In case *message_ids* was not
            a list, a single result is returned, otherwise a list of results is returned.

        Example:
            .. code-block:: python

                await app.translate_text("fa", "Pyrogram")
        """
        message, entities = (
            await utils.parse_text_entities(self, text, parse_mode, entities)
        ).values()

        r = await self.invoke(
            raw.functions.messages.TranslateText(
                to_lang=to_language_code,
                text=[
                    raw.types.TextWithEntities(
                        text=message,
                        entities=entities or [],
                    ),
                ],
            ),
        )

        return (
            types.TranslatedText._parse(self, r.result[0])
            if len(r.result) == 1
            else [types.TranslatedText._parse(self, i) for i in r.result]
        )
