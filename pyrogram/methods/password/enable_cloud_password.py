from __future__ import annotations

import os

import pyrogram
from pyrogram import raw
from pyrogram.utils import btoi, compute_password_hash, itob


class EnableCloudPassword:
    async def enable_cloud_password(
        self: pyrogram.Client,
        password: str,
        hint: str = "",
        email: str | None = None,
    ) -> bool:
        """Enable the Two-Step Verification security feature (Cloud Password) on your account.

        This password will be asked when you log-in on a new device in addition to the SMS code.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            password (``str``):
                Your password.

            hint (``str``, *optional*):
                A password hint.

            email (``str``, *optional*):
                Recovery e-mail.

        Returns:
            ``bool``: True on success.

        Raises:
            ValueError: In case there is already a cloud password enabled.

        Example:
            .. code-block:: python

                # Enable password without hint and email
                await app.enable_cloud_password("password")

                # Enable password with hint and without email
                await app.enable_cloud_password("password", hint="hint")

                # Enable password with hint and email
                await app.enable_cloud_password("password", hint="hint", email="user@email.com")
        """
        r = await self.invoke(raw.functions.account.GetPassword())

        if r.has_password:
            raise ValueError("There is already a cloud password enabled")

        r.new_algo.salt1 += os.urandom(32)
        new_hash = btoi(compute_password_hash(r.new_algo, password))
        new_hash = itob(pow(r.new_algo.g, new_hash, btoi(r.new_algo.p)))

        await self.invoke(
            raw.functions.account.UpdatePasswordSettings(
                password=raw.types.InputCheckPasswordEmpty(),
                new_settings=raw.types.account.PasswordInputSettings(
                    new_algo=r.new_algo,
                    new_password_hash=new_hash,
                    hint=hint,
                    email=email,
                ),
            ),
        )

        return True
