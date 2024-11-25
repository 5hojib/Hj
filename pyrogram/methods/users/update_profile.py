from __future__ import annotations

import pyrogram
from pyrogram import raw


class UpdateProfile:
    async def update_profile(
        self: pyrogram.Client,
        first_name: str | None = None,
        last_name: str | None = None,
        bio: str | None = None,
    ) -> bool:
        """Update your profile details such as first name, last name and bio.

        You can omit the parameters you don't want to change.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            first_name (``str``, *optional*):
                The new first name.

            last_name (``str``, *optional*):
                The new last name.
                Pass "" (empty string) to remove it.

            bio (``str``, *optional*):
                The new bio, also known as "about". Max 70 characters.
                Pass "" (empty string) to remove it.

        Returns:
            ``bool``: True on success.

        Example:
            .. code-block:: python

                # Update your first name only
                await app.update_profile(first_name="5hojib")

                # Update first name and bio
                await app.update_profile(first_name="5hojib", bio="I love you 💖")

                # Remove the last name
                await app.update_profile(last_name="")
        """

        return bool(
            await self.invoke(
                raw.functions.account.UpdateProfile(
                    first_name=first_name,
                    last_name=last_name,
                    about=bio,
                ),
            ),
        )
