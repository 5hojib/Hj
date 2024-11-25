from __future__ import annotations

import re

import pyrogram
from pyrogram import raw, types


class GetPaymentForm:
    async def get_payment_form(
        self: pyrogram.Client,
        chat_id: int | str,
        message_id: int | str,
    ) -> types.PaymentForm:
        """Get information about a invoice or paid media.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                Unique identifier for the target chat in form of a *t.me/joinchat/* link, identifier (int) or username
                of the target channel/supergroup (in the format @username).
            message_id (``int`` | ``str``):
                Pass a message identifier or to get the invoice from message.
                Pass a invoice link in form of a *t.me/$...* link or slug itself to get the payment form from link.

        Returns:
            :obj:`~pyrogram.types.PaymentForm`: On success, a payment form is returned.

        Example:
            .. code-block:: python

                # get payment form from message
                app.get_payment_form(chat_id, 123)
                # get payment form from link
                app.get_payment_form(chat_id, "https://t.me/$xvbzUtt5sUlJCAAATqZrWRy9Yzk")
        """
        invoice = None

        if isinstance(message_id, int):
            invoice = raw.types.InputInvoiceMessage(
                peer=await self.resolve_peer(chat_id),
                msg_id=message_id,
            )
        elif isinstance(message_id, str):
            match = re.match(
                r"^(?:https?://)?(?:www\.)?(?:t(?:elegram)?\.(?:org|me|dog)/\$)([\w-]+)$",
                message_id,
            )

            slug = match.group(1) if match else message_id

            invoice = raw.types.InputInvoiceSlug(slug=slug)

        r = await self.invoke(raw.functions.payments.GetPaymentForm(invoice=invoice))

        return types.PaymentForm._parse(self, r)
