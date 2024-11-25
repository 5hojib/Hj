from __future__ import annotations

import pyrogram
from pyrogram import raw, types
from pyrogram.types.object import Object


class MessageReactor(Object):
    """Contains information about a message reactor.
    Parameters:
        amount (``int``):
            Stars amount.

        is_top (``bool``, *optional*):
            True, if reactor is top.

        is_my (``bool``, *optional*):
            True, if the reaction is mine.

        is_anonymous (``bool``, *optional*):
            True, if reactor is anonymous.

        from_user (:obj:`~pyrogram.types.User`, *optional*):
            Information about the reactor.
    """

    def __init__(
        self,
        *,
        client: pyrogram.Client = None,
        amount: int,
        is_top: bool | None = None,
        is_my: bool | None = None,
        is_anonymous: bool | None = None,
        from_user: types.User = None,
    ) -> None:
        super().__init__(client)

        self.amount = amount
        self.is_top = is_top
        self.is_my = is_my
        self.is_anonymous = is_anonymous
        self.from_user = from_user

    @staticmethod
    def _parse(
        client: pyrogram.Client,
        message_reactor: raw.base.MessageReactor | None = None,
        users: dict[int, raw.types.User] | None = None,
    ) -> MessageReactor | None:
        if not message_reactor:
            return None

        is_anonymous = message_reactor.anonymous
        from_user = None
        if not is_anonymous:
            from_user = types.User._parse(
                client,
                users.get(message_reactor.peer_id.user_id),
            )

        return MessageReactor(
            client=client,
            amount=message_reactor.count,
            is_top=message_reactor.top,
            is_my=message_reactor.my,
            is_anonymous=is_anonymous,
            from_user=from_user,
        )
