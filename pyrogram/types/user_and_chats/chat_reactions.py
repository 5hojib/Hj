from __future__ import annotations

import pyrogram
from pyrogram import raw, types
from pyrogram.types.object import Object


class ChatReactions(Object):
    """A chat reactions

    Parameters:
        all_are_enabled (``bool``, *optional*)

        allow_custom_emoji (``bool``, *optional*):
            Whether custom emoji are allowed or not.

        reactions (List of :obj:`~pyrogram.types.Reaction`, *optional*):
            Reactions available.

        max_reaction_count (``int``, *optional*):
            Limit of the number of different unique reactions that can be added to a message, including already published ones. Can have values between 1 and 11. Defaults to 11, if not specified. Only applicable for :obj:`~pyrogram.enums.ChatType.CHANNEL`.
    """

    def __init__(
        self,
        *,
        client: pyrogram.Client = None,
        all_are_enabled: bool | None = None,
        allow_custom_emoji: bool | None = None,
        reactions: list[types.Reaction] | None = None,
        max_reaction_count: int = 11,
    ) -> None:
        super().__init__(client)

        self.all_are_enabled = all_are_enabled
        self.allow_custom_emoji = allow_custom_emoji
        self.reactions = reactions
        self.max_reaction_count = max_reaction_count

    @staticmethod
    def _parse(
        client,
        chat_reactions: raw.base.ChatReactions,
        reactions_limit: int = 11,
    ) -> ChatReactions | None:
        if isinstance(chat_reactions, raw.types.ChatReactionsAll):
            return ChatReactions(
                client=client,
                all_are_enabled=True,
                allow_custom_emoji=chat_reactions.allow_custom,
                max_reaction_count=reactions_limit,
            )

        if isinstance(chat_reactions, raw.types.ChatReactionsSome):
            return ChatReactions(
                client=client,
                reactions=[
                    types.ReactionType._parse(client, reaction)
                    for reaction in chat_reactions.reactions
                ],
                max_reaction_count=reactions_limit,
            )

        if isinstance(chat_reactions, raw.types.ChatReactionsNone):
            return None

        return None
