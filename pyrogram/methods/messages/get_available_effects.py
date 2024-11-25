from __future__ import annotations

import logging

import pyrogram
from pyrogram import raw, types

log = logging.getLogger(__name__)


class GetAvailableEffects:
    async def get_available_effects(
        self: pyrogram.Client,
    ) -> list[types.AvailableEffect]:
        """Get all available effects.

        .. include:: /_includes/usable-by/users.rst

        Returns:
            List of :obj:`~pyrogram.types.AvailableEffect`: A list of available effects is returned.

        Example:
            .. code-block:: python

                # Get all available effects
                await app.get_available_effects()
        """
        r = await self.invoke(raw.functions.messages.GetAvailableEffects(hash=0))

        documents = {d.id: d for d in r.documents}

        return types.List(
            [
                await types.AvailableEffect._parse(
                    self,
                    effect,
                    documents.get(effect.effect_sticker_id, None),
                )
                for effect in r.effects
            ],
        )
