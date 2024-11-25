from __future__ import annotations

import pyrogram
from pyrogram.types.object import Object


class PollOption(Object):
    """Contains information about one answer option in a poll.

    Parameters:
        text (``str``):
            Option text, 1-100 characters.

        voter_count (``int``, *optional*):
            Number of users that voted for this option.
            Equals to 0 until you vote.

        data (``bytes``, *optional*):
            The data this poll option is holding.

        entities (List of :obj:`~pyrogram.types.MessageEntity`, *optional*):
            Special entities like usernames, URLs, bot commands, etc. that appear in the option text.
    """

    def __init__(
        self,
        *,
        client: pyrogram.Client = None,
        text: str,
        voter_count: int = 0,
        data: bytes | None = None,
        entities: list[pyrogram.types.MessageEntity] | None = None,
    ) -> None:
        super().__init__(client)

        self.text = text
        self.voter_count = voter_count
        self.data = data
        self.entities = entities

    async def write(self, client, i):
        option, entities = (
            await pyrogram.utils.parse_text_entities(
                client,
                self.text,
                None,
                self.entities,
            )
        ).values()
        return pyrogram.raw.types.PollAnswer(
            text=pyrogram.raw.types.TextWithEntities(
                text=option,
                entities=entities or [],
            ),
            option=bytes([i]),
        )
