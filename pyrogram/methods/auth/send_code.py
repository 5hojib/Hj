from __future__ import annotations

import logging

import pyrogram
from pyrogram import raw, types
from pyrogram.errors import NetworkMigrate, PhoneMigrate
from pyrogram.session import Auth, Session

log = logging.getLogger(__name__)


class SendCode:
    async def send_code(self: pyrogram.Client, phone_number: str) -> types.SentCode:
        """Send the confirmation code to the given phone number.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            phone_number (``str``):
                Phone number in international format (includes the country prefix).

        Returns:
            :obj:`~pyrogram.types.SentCode`: On success, an object containing information on the sent confirmation code
            is returned.

        Raises:
            BadRequest: In case the phone number is invalid.
        """
        phone_number = phone_number.strip(" +")

        while True:
            try:
                r = await self.invoke(
                    raw.functions.auth.SendCode(
                        phone_number=phone_number,
                        api_id=self.api_id,
                        api_hash=self.api_hash,
                        settings=raw.types.CodeSettings(),
                    ),
                )
            except (PhoneMigrate, NetworkMigrate) as e:
                await self.session.stop()

                await self.storage.dc_id(e.value)
                await self.storage.auth_key(
                    await Auth(
                        self,
                        await self.storage.dc_id(),
                        await self.storage.test_mode(),
                    ).create(),
                )
                self.session = Session(
                    self,
                    await self.storage.dc_id(),
                    await self.storage.auth_key(),
                    await self.storage.test_mode(),
                )

                await self.session.start()
            else:
                return types.SentCode._parse(r)
