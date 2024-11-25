from __future__ import annotations

import logging

import pyrogram
from pyrogram import raw, types

log = logging.getLogger(__name__)


class ResendCode:
    async def resend_code(
        self: pyrogram.Client,
        phone_number: str,
        phone_code_hash: str,
    ) -> types.SentCode:
        """Re-send the confirmation code using a different type.

        The type of the code to be re-sent is specified in the *next_type* attribute of the
        :obj:`~pyrogram.types.SentCode` object returned by :meth:`send_code`.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            phone_number (``str``):
                Phone number in international format (includes the country prefix).

            phone_code_hash (``str``):
                Confirmation code identifier.

        Returns:
            :obj:`~pyrogram.types.SentCode`: On success, an object containing information on the re-sent confirmation
            code is returned.

        Raises:
            BadRequest: In case the arguments are invalid.
        """
        phone_number = phone_number.strip(" +")

        r = await self.invoke(
            raw.functions.auth.ResendCode(
                phone_number=phone_number,
                phone_code_hash=phone_code_hash,
            ),
        )

        return types.SentCode._parse(r)
