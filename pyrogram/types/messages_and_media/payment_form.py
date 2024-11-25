from __future__ import annotations

import pyrogram
from pyrogram import raw, types
from pyrogram.types.object import Object


class PaymentForm(Object):
    """This object contains basic information about an payment form.

    Parameters:
        id (``int``):
            Form id.

        bot (``str``):
            Bot.

        title (``str``):
            Form title.

        description (``str``):
            Form description.

        invoice (``str``):
            Invoice.

        provider (``str``, *optional*):
            Payment provider.

        url (``str``, *optional*):
            Payment form URL.

        can_save_credentials (``str``, *optional*):
            Whether the user can choose to save credentials.

        is_password_missing (``str``, *optional*):
            Indicates that the user can save payment credentials,
            but only after setting up a 2FA password
            (currently the account doesn't have a 2FA password).

        native_provider (``str``, *optional*):
            Payment provider name.

        raw (:obj:`~raw.base.payments.PaymentForm`, *optional*):
            The raw object, as received from the Telegram API.
    """

    def __init__(
        self,
        *,
        client: pyrogram.Client = None,
        id: int,
        bot: types.User,
        title: str,
        description: str,
        invoice: types.Invoice,
        provider: types.User | None = None,
        url: str | None = None,
        can_save_credentials: bool | None = None,
        is_password_missing: bool | None = None,
        native_provider: str | None = None,
        raw: raw.base.payments.PaymentForm = None,
        # TODO: Add support for other params:
        # native_params
        # additional_params
        # saved_info
        # saved_credentials
    ) -> None:
        super().__init__(client)

        self.id = id
        self.bot = bot
        self.title = title
        self.description = description
        self.invoice = invoice
        self.provider = provider
        self.url = url
        self.can_save_credentials = can_save_credentials
        self.is_password_missing = is_password_missing
        self.native_provider = native_provider
        self.raw = raw

    @staticmethod
    def _parse(client, payment_form: raw.base.payments.PaymentForm) -> PaymentForm:
        users = {i.id: i for i in payment_form.users}

        return PaymentForm(
            id=payment_form.form_id,
            bot=types.User._parse(client, users.get(payment_form.bot_id)),
            title=payment_form.title,
            description=payment_form.description,
            invoice=types.Invoice._parse(client, payment_form.invoice),
            provider=types.User._parse(
                client,
                users.get(getattr(payment_form, "provider_id", None)),
            ),
            url=getattr(payment_form, "url", None),
            can_save_credentials=getattr(payment_form, "can_save_credentials", None),
            is_password_missing=getattr(payment_form, "password_missing", None),
            native_provider=getattr(payment_form, "native_provider", None),
            raw=payment_form,
        )
