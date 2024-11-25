from __future__ import annotations

import pyrogram
from pyrogram import raw
from pyrogram.utils import compute_password_check


class DeleteAccount:
    async def delete_account(
        self: pyrogram.Client,
        reason: str = "",
        password: str | None = None,
    ) -> bool:
        """Deletes the account of the current user, deleting all information associated with the user from the server.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            reason (``str``, *optional*):
                The reason why the account was deleted.

            password (``str``, *optional*):
                The 2-step verification password of the current user. If the current user isn't authorized, then an empty string can be passed and account deletion can be canceled within one week.

        Returns:
            `bool`: True On success.

        Example:
            .. code-block:: python

                await app.delete_account(reason, password)
        """
        r = await self.invoke(
            raw.functions.account.DeleteAccount(
                reason=reason,
                password=compute_password_check(
                    await self.invoke(raw.functions.account.GetPassword()),
                    password,
                )
                if password
                else None,
            ),
        )

        return bool(r)
