from __future__ import annotations

import pyrogram
from pyrogram import raw, types


class SendReaction:
    async def send_reaction(
        self: pyrogram.Client,
        chat_id: int | str,
        message_id: int | None = None,
        story_id: int | None = None,
        emoji: int | str | list[int | str] | None = None,
        big: bool = False,
        add_to_recent: bool = False,
    ) -> types.MessageReactions:
        """Use this method to send reactions on a message/stories.
        Service messages can't be reacted to.
        Automatically forwarded messages from
        a channel to its discussion group have the
        same available reactions as messages in the channel.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                You can also use chat public link in form of *t.me/<username>* (str).

            message_id (``int``, *optional*):
                Identifier of the target message. If the message belongs to a media group, the reaction is set to the first non-deleted message in the group instead.

            story_id (``int``, *optional*):
                Identifier of the story.

            emoji (``int`` | ``str`` | List of ``int`` | ``str``, *optional*):
                Reaction emoji.
                Pass None as emoji (default) to retract the reaction.
                Pass list of int or str to react multiple emojis.

            big (``bool``, *optional*):
                Pass True to set the reaction with a big animation.
                For message reactions only.
                Defaults to False.

            add_to_recent (``bool``, *optional*):
                Pass True if the reaction should appear in the recently used reactions.
                This option is applicable only for users.

        Returns:
            :obj:`~pyrogram.types.MessageReactions`: On success, True is returned.

        Example:
            .. code-block:: python

                # Send a reaction
                await app.send_reaction(chat_id, message_id=message_id, emoji="🔥")
                await app.send_reaction(chat_id, story_id=story_id, emoji="🔥")

                # Send a multiple reactions
                await app.send_reaction(chat_id, message_id=message_id, emoji=["🔥", "❤️"])

                # Retract a reaction
                await app.send_reaction(chat_id, message_id=message_id)
                await app.send_reaction(chat_id, story_id=story_id)
        """
        if isinstance(emoji, list):
            reaction = (
                [
                    raw.types.ReactionCustomEmoji(document_id=i)
                    if isinstance(i, int)
                    else raw.types.ReactionEmoji(emoticon=i)
                    for i in emoji
                ]
                if emoji
                else None
            )
        elif isinstance(emoji, int):
            reaction = [raw.types.ReactionCustomEmoji(document_id=emoji)]
        else:
            reaction = [raw.types.ReactionEmoji(emoticon=emoji)] if emoji else None
        if message_id is not None:
            r = await self.invoke(
                raw.functions.messages.SendReaction(
                    peer=await self.resolve_peer(chat_id),
                    msg_id=message_id,
                    reaction=reaction,
                    big=big,
                    add_to_recent=add_to_recent,
                ),
            )
            for i in r.updates:
                if isinstance(i, raw.types.UpdateMessageReactions):
                    return types.MessageReactions._parse(self, i.reactions)
            return None
        if story_id is not None:
            await self.invoke(
                raw.functions.stories.SendReaction(
                    peer=await self.resolve_peer(chat_id),
                    story_id=story_id,
                    reaction=raw.types.ReactionEmoji(emoticon=emoji)
                    if emoji
                    else None,
                    add_to_recent=add_to_recent,
                ),
            )
            return True
        raise ValueError("You need to pass one of message_id!")
