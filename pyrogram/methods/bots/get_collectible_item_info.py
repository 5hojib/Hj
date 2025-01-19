from __future__ import annotations

import pyrogram
from pyrogram import raw, types


class GetCollectibleItemInfo:
    async def get_collectible_item_info(
        self: pyrogram.Client,
        username: str | None = None,
        phone_number: str | None = None,
    ) -> types.CollectibleInfo:
        """Returns information about a given collectible item that was purchased at https://fragment.com

        .. include:: /_includes/usable-by/users.rst

        You must use exactly one of ``username`` OR ``phone_number``.

        Parameters:
            username (``str``, *optional*):
                Describes a collectible username that can be purchased at https://fragment.com
            phone_number (``str``, *optional*):
                Describes a collectible phone number that can be purchased at https://fragment.com

        Returns:
            :obj:`~pyrogram.types.CollectibleInfo`: On success, a collectible info is returned.

        Example:
            .. code-block:: python

                username = await app.get_collectible_item_info(username="nerd")
                print(username)
        """

        input_collectible = None

        if username:
            input_collectible = raw.types.InputCollectibleUsername(username=username)
        elif phone_number:
            input_collectible = raw.types.InputCollectiblePhone(phone=phone_number)
        else:
            raise ValueError(
                "No argument supplied. Either pass username OR phone_number",
            )

        r = await self.invoke(
            raw.functions.fragment.GetCollectibleInfo(collectible=input_collectible),
        )

        return types.CollectibleItemInfo._parse(r)
