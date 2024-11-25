from __future__ import annotations

from typing import TYPE_CHECKING

import pyrogram
from pyrogram import raw, types, utils
from pyrogram.types.object import Object
from pyrogram.types.update import Update

if TYPE_CHECKING:
    from datetime import datetime


class MessageReactionUpdated(Object, Update):
    """This object represents a change of a reaction on a message performed by a user.
    A reaction to a message was changed by a user.
    The update isn't received for reactions set by bots.

    These updates are heavy and their changes may be delayed by a few minutes.

    Parameters:
        id (``int``):
            Unique identifier of the message inside the chat

        chat (:obj:`~pyrogram.types.Chat`):
            The chat containing the message the user reacted to

        from_user (:obj:`~pyrogram.types.User`, *optional*):
            The user that changed the reaction, if the user isn't anonymous

        actor_chat (:obj:`~pyrogram.types.Chat`, *optional*):
            The chat on behalf of which the reaction was changed, if the user is anonymous

        date (:py:obj:`~datetime.datetime`):
            Date of change of the reaction

        old_reaction (:obj:`~pyrogram.types.ReactionType`):
            Previous list of reaction types that were set by the user

        new_reaction (:obj:`~pyrogram.types.ReactionType`):
            New list of reaction types that have been set by the user

    """

    def __init__(
        self,
        *,
        client: pyrogram.Client = None,
        id: int,
        from_user: types.User,
        actor_chat: types.Chat,
        date: datetime,
        chat: types.Chat,
        old_reaction: list[types.ReactionType],
        new_reaction: list[types.ReactionType],
    ) -> None:
        super().__init__(client)

        self.id = id
        self.from_user = from_user
        self.actor_chat = actor_chat
        self.date = date
        self.chat = chat
        self.old_reaction = old_reaction
        self.new_reaction = new_reaction

    @staticmethod
    def _parse(
        client: pyrogram.Client,
        update: raw.types.UpdateBotMessageReaction,
        users: dict[int, raw.types.User],
        chats: dict[int, raw.types.Chat],
    ) -> MessageReactionUpdated:
        chat = None
        peer_id = utils.get_peer_id(update.peer)
        raw_peer_id = utils.get_raw_peer_id(update.peer)
        if peer_id > 0:
            chat = types.Chat._parse_user_chat(client, users[raw_peer_id])
        else:
            chat = types.Chat._parse_channel_chat(client, chats[raw_peer_id])

        from_user = None
        actor_chat = None

        raw_actor_peer_id = utils.get_raw_peer_id(update.actor)
        actor_peer_id = utils.get_peer_id(update.actor)

        if actor_peer_id > 0:
            from_user = types.User._parse(client, users[raw_actor_peer_id])
        else:
            actor_chat = types.Chat._parse_channel_chat(
                client,
                chats[raw_actor_peer_id],
            )

        return MessageReactionUpdated(
            client=client,
            id=update.msg_id,
            from_user=from_user,
            date=utils.timestamp_to_datetime(update.date),
            chat=chat,
            actor_chat=actor_chat,
            old_reaction=[
                types.ReactionType._parse(client, rt) for rt in update.old_reactions
            ],
            new_reaction=[
                types.ReactionType._parse(client, rt) for rt in update.new_reactions
            ],
        )
