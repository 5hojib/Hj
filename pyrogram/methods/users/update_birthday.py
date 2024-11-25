from __future__ import annotations

import pyrogram
from pyrogram import raw, types


class UpdateBirthday:
    async def update_birthday(
        self: pyrogram.Client,
        day: int,
        month: int,
        year: int | None = None,
    ) -> bool:
        """Update your birthday details.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            day (``int``):
                Day of birth.

            month (``int``):
                Month of birth.

            year (``int``, *optional*):
                Year of birth.

        Returns:
            ``bool``: True on success.

        Example:
            .. code-block:: python

                # Update your birthday to 1st January 2000
                # 1874/01/01(YMD) is the earliest date, earlier will raise 400 Bad Request BIRTHDAY_INVALID.
                await app.update_birthday(day=1, month=1, year=2000)
        """
        birthday = types.Birthday(day=day, month=month, year=year)
        birthday = await birthday.write()

        r = await self.invoke(
            raw.functions.account.UpdateBirthday(birthday=birthday),
        )
        return bool(r)
