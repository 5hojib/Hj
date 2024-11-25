from __future__ import annotations

from pyrogram import raw, utils
from pyrogram.types.object import Object


class SentWebAppMessage(Object):
    """Contains information about an inline message sent by a `Web App <https://core.telegram.org/bots/webapps>`_ on behalf of a user.

    Parameters:
        inline_message_id (``str``):
            Identifier of the sent inline message.
            Available only if there is an inline keyboard attached to the message.
    """

    def __init__(
        self,
        *,
        inline_message_id: str,
    ) -> None:
        super().__init__()

        self.inline_message_id = inline_message_id

    @staticmethod
    def _parse(obj: raw.types.WebViewMessageSent):
        return SentWebAppMessage(
            inline_message_id=utils.pack_inline_message_id(obj.msg_id),
        )
