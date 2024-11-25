from __future__ import annotations

import os

import pyrogram
from pyrogram import raw
from pyrogram.utils import (
    btoi,
    compute_password_check,
    compute_password_hash,
    itob,
)


class ChangeCloudPassword:
    async def change_cloud_password(
        self: pyrogram.Client,
        current_password: str,
        new_password: str,
        new_hint: str = "",
    ) -> bool:
        """Change your Two-Step Verification password (Cloud Password) with a new one.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            current_password (``str``):
                Your current password.

            new_password (``str``):
                Your new password.

            new_hint (``str``, *optional*):
                A new password hint.

        Returns:
            ``bool``: True on success.

        Raises:
            ValueError: In case there is no cloud password to change.

        Example:
            .. code-block:: python

                # Change password only
                await app.change_cloud_password("current_password", "new_password")

                # Change password and hint
                await app.change_cloud_password("current_password", "new_password", new_hint="hint")
        """
        r = await self.invoke(raw.functions.account.GetPassword())

        if not r.has_password:
            raise ValueError("There is no cloud password to change")

        r.new_algo.salt1 += os.urandom(32)
        new_hash = btoi(compute_password_hash(r.new_algo, new_password))
        new_hash = itob(pow(r.new_algo.g, new_hash, btoi(r.new_algo.p)))

        await self.invoke(
            raw.functions.account.UpdatePasswordSettings(
                password=compute_password_check(r, current_password),
                new_settings=raw.types.account.PasswordInputSettings(
                    new_algo=r.new_algo,
                    new_password_hash=new_hash,
                    hint=new_hint,
                ),
            ),
        )

        return True
