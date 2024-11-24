from __future__ import annotations

from .answer_pre_checkout_query import AnswerPreCheckoutQuery
from .answer_shipping_query import AnswerShippingQuery
from .create_invoice_link import CreateInvoiceLink
from .get_available_gifts import GetAvailableGifts
from .get_business_connection import GetBusinessConnection
from .get_payment_form import GetPaymentForm
from .get_stars_transactions import GetStarsTransactions
from .get_stars_transactions_by_id import GetStarsTransactionsById
from .get_user_gifts import GetUserGifts
from .refund_stars_payment import RefundStarPayment
from .sell_gift import SellGift
from .send_gift import SendGift
from .send_invoice import SendInvoice
from .send_payment_form import SendPaymentForm
from .toggle_gift_is_saved import ToggleGiftIsSaved


class TelegramBusiness(
    AnswerPreCheckoutQuery,
    AnswerShippingQuery,
    CreateInvoiceLink,
    GetBusinessConnection,
    GetAvailableGifts,
    GetUserGifts,
    SellGift,
    SendGift,
    ToggleGiftIsSaved,
    GetStarsTransactions,
    GetStarsTransactionsById,
    RefundStarPayment,
    SendInvoice,
    GetPaymentForm,
    SendPaymentForm,
):
    pass
