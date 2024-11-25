from __future__ import annotations

import logging

import pyrogram
from pyrogram import raw, types
from pyrogram.utils import compute_password_check

log = logging.getLogger(__name__)


class CheckPassword:
    async def check_password(self: pyrogram.Client, password: str) -> types.User:
        """Check your Two-Step Verification password and log in.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            password (``str``):
                Your Two-Step Verification password.

        Returns:
            :obj:`~pyrogram.types.User`: On success, the authorized user is returned.

        Raises:
            BadRequest: In case the password is invalid.
        """
        r = await self.invoke(
            raw.functions.auth.CheckPassword(
                password=compute_password_check(
                    await self.invoke(raw.functions.account.GetPassword()),
                    password,
                ),
            ),
        )

        await self.storage.user_id(r.user.id)
        await self.storage.is_bot(False)

        return types.User._parse(self, r.user)
