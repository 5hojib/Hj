from __future__ import annotations

from typing import TYPE_CHECKING

import pyrogram
from pyrogram import raw, types, utils
from pyrogram.types.messages_and_media.message import Str
from pyrogram.types.object import Object

if TYPE_CHECKING:
    from datetime import datetime


class UserGift(Object):
    """Represents a gift received by a user.

    Parameters:
        sender_user (:obj:`~pyrogram.types.User`, *optional*):
            Identifier of the user that sent the gift; None if unknown.

        text (``str``, *optional*):
            Message added to the gift.

        entities (List of :obj:`~pyrogram.types.MessageEntity`, *optional*):
            For text messages, special entities like usernames, URLs, bot commands, etc. that appear in the text.

        is_private (``bool``, *optional*):
            True, if the sender and gift text are shown only to the gift receiver; otherwise, everyone are able to see them.

        is_saved (``bool``, *optional*):
            True, if the gift is displayed on the user's profile page; may be False only for the receiver of the gift.

        date (``datetime``):
            Date when the gift was sent.

        gift (:obj:`~pyrogram.types.Gift`, *optional*):
            Information about the gift.

        message_id (``int``, *optional*):
            Identifier of the message with the gift in the chat with the sender of the gift; can be None or an identifier of a deleted message; only for the gift receiver.

        sell_star_count (``int``, *optional*):
            Number of Telegram Stars that can be claimed by the receiver instead of the gift; only for the gift receiver.

    """

    def __init__(
        self,
        *,
        client: pyrogram.Client = None,
        sender_user: types.User | None = None,
        text: str | None = None,
        entities: list[types.MessageEntity] | None = None,
        date: datetime,
        is_private: bool | None = None,
        is_saved: bool | None = None,
        gift: types.Gift | None = None,
        message_id: int | None = None,
        sell_star_count: int | None = None,
    ) -> None:
        super().__init__(client)

        self.date = date
        self.gift = gift
        self.is_private = is_private
        self.is_saved = is_saved
        self.sender_user = sender_user
        self.text = text
        self.entities = entities
        self.message_id = message_id
        self.sell_star_count = sell_star_count

    @staticmethod
    async def _parse(
        client,
        user_star_gift: raw.types.UserStarGift,
        users: dict,
    ) -> UserGift:
        text, entities = None, None
        if getattr(user_star_gift, "message", None):
            text = user_star_gift.message.text or None
            entities = [
                types.MessageEntity._parse(client, entity, users)
                for entity in user_star_gift.message.entities
            ]
            entities = types.List(filter(lambda x: x is not None, entities))

        return UserGift(
            date=utils.timestamp_to_datetime(user_star_gift.date),
            gift=await types.Gift._parse(client, user_star_gift.gift),
            is_private=getattr(user_star_gift, "name_hidden", None),
            is_saved=not user_star_gift.unsaved
            if getattr(user_star_gift, "unsaved", None)
            else None,
            sender_user=types.User._parse(client, users.get(user_star_gift.from_id))
            if getattr(user_star_gift, "from_id", None)
            else None,
            message_id=getattr(user_star_gift, "msg_id", None),
            sell_star_count=getattr(user_star_gift, "convert_stars", None),
            text=Str(text).init(entities) if text else None,
            entities=entities,
            client=client,
        )

    @staticmethod
    async def _parse_action(
        client,
        message: raw.base.Message,
        users: dict,
    ) -> UserGift:
        action = message.action

        doc = action.gift.sticker
        attributes = {type(i): i for i in doc.attributes}

        text, entities = None, None
        if getattr(action, "message", None):
            text = action.message.text or None
            entities = [
                types.MessageEntity._parse(client, entity, users)
                for entity in action.message.entities
            ]
            entities = types.List(filter(lambda x: x is not None, entities))

        return UserGift(
            gift=types.Gift(
                id=action.gift.id,
                sticker=await types.Sticker._parse(client, doc, attributes),
                star_count=action.gift.stars,
                default_sell_star_count=action.gift.convert_stars,
                remaining_count=getattr(action.gift, "availability_remains", None),
                total_count=getattr(action.gift, "availability_total", None),
                is_limited=getattr(action.gift, "limited", None),
            ),
            date=utils.timestamp_to_datetime(message.date),
            is_private=getattr(action, "name_hidden", None),
            is_saved=getattr(action, "saved", None),
            sender_user=types.User._parse(
                client,
                users.get(utils.get_raw_peer_id(message.peer_id)),
            ),
            message_id=message.id,
            text=Str(text).init(entities) if text else None,
            entities=entities,
            client=client,
        )

    async def toggle(self, is_saved: bool) -> bool:
        """Bound method *toggle* of :obj:`~pyrogram.types.UserGift`.

        Use as a shortcut for:

        .. code-block:: python

            await client.toggle_gift_is_saved(
                sender_user_id=user_id,
                message_id=message_id
            )

        Parameters:
            is_saved (``bool``):
                Pass True to display the gift on the user's profile page; pass False to remove it from the profile page.

        Example:
            .. code-block:: python

                await user_gift.toggle(is_saved=False)

        Returns:
            ``bool``: On success, True is returned.

        """
        return await self._client.toggle_gift_is_saved(
            sender_user_id=self.sender_user.id,
            message_id=self.message_id,
            is_saved=is_saved,
        )
