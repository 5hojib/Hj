from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

import pyrogram
from pyrogram import raw, types, utils
from pyrogram.errors import FloodWait
from pyrogram.types.object import Object

if TYPE_CHECKING:
    from datetime import datetime


class Giveaway(Object):
    """A giveaway.

    Parameters:
        chats (List of :obj:`~pyrogram.types.Chat`):
            List of channel(s) which host the giveaway.

        quantity (``int``):
            Quantity of the giveaway prize.

        months (``int``):
            How long the telegram premium last (in month).

        expire_date (:py:obj:`~datetime.datetime`):
            Date the giveaway winner(s) will be choosen.

        new_subscribers (``bool``):
            True, if the giveaway only for new subscribers.

        allowed_countries (List of ``str``, *optional*):
            List of ISO country codes which eligible to join the giveaway.

        private_channel_ids (List of ``int``, *optional*):
            List of Unique channel identifier of private channel which host the giveaway.
    """

    def __init__(
        self,
        *,
        client: pyrogram.Client = None,
        chats: list[types.Chat],
        quantity: int,
        months: int,
        expire_date: datetime,
        new_subscribers: bool,
        allowed_countries: list[str] | None = None,
        private_channel_ids: list[int] | None = None,
    ) -> None:
        super().__init__(client)

        self.chats = chats
        self.quantity = quantity
        self.months = months
        self.expire_date = expire_date
        self.new_subscribers = new_subscribers
        self.allowed_countries = allowed_countries
        self.private_channel_ids = private_channel_ids

    @staticmethod
    async def _parse(client, message: raw.types.Message) -> Giveaway:
        giveaway: raw.types.MessageMediaGiveaway = message.media
        chats = []
        private_ids = []
        for raw_chat_id in giveaway.channels:
            chat_id = utils.get_channel_id(raw_chat_id)
            try:
                chat = await client.invoke(
                    raw.functions.channels.GetChannels(
                        id=[await client.resolve_peer(chat_id)],
                    ),
                )
            except FloodWait as e:
                await asyncio.sleep(e.value)
            except Exception:
                private_ids.append(chat_id)
            else:
                chats.append(types.Chat._parse_chat(client, chat.chats[0]))

        return Giveaway(
            chats=chats,
            quantity=giveaway.quantity,
            months=giveaway.months,
            expire_date=utils.timestamp_to_datetime(giveaway.until_date),
            new_subscribers=giveaway.only_new_subscribers,
            allowed_countries=giveaway.countries_iso2
            if len(giveaway.countries_iso2) > 0
            else None,
            private_channel_ids=private_ids if len(private_ids) > 0 else None,
            client=client,
        )
