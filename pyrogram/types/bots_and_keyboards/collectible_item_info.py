from __future__ import annotations

from typing import TYPE_CHECKING

from pyrogram import raw, utils
from pyrogram.types.object import Object

if TYPE_CHECKING:
    from datetime import datetime


class CollectibleItemInfo(Object):
    """Contains information about a collectible item and its last purchase.
    Parameters:
        purchase_date (``datetime``):
            Point in time (Unix timestamp) when the item was purchased
        currency (``str``):
            Currency for the paid amount
        amount (``float``):
            The paid amount, in the smallest units of the currency
        cryptocurrency (``str``):
            Cryptocurrency used to pay for the item
        cryptocurrency_amount (``float``):
            The paid amount, in the smallest units of the cryptocurrency
        url (``str``):
            Individual URL for the item on https://fragment.com

    """

    def __init__(
        self,
        *,
        purchase_date: datetime,
        currency: str,
        amount: float,
        cryptocurrency: str,
        cryptocurrency_amount: float,
        url: str,
    ) -> None:
        super().__init__()

        self.purchase_date = purchase_date
        self.currency = currency
        self.amount = amount
        self.cryptocurrency = cryptocurrency
        self.cryptocurrency_amount = cryptocurrency_amount
        self.url = url

    @staticmethod
    def _parse(
        collectible_info: raw.types.fragment.CollectibleInfo,
    ) -> CollectibleItemInfo:
        return CollectibleItemInfo(
            purchase_date=utils.timestamp_to_datetime(
                collectible_info.purchase_date,
            ),
            currency=collectible_info.currency,
            amount=collectible_info.amount,
            cryptocurrency=collectible_info.crypto_currency,
            cryptocurrency_amount=collectible_info.crypto_amount,
            url=collectible_info.url,
        )
