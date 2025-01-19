from __future__ import annotations

from json import dumps
from random import randint

import pyrogram
from pyrogram import enums, raw


class SendChatAction:
    async def send_chat_action(
        self: pyrogram.Client,
        chat_id: int | str,
        action: enums.ChatAction,
        message_thread_id: int | None = None,
        business_connection_id: str | None = None,
        emoji: str | None = None,
        emoji_message_id: int | None = None,
        emoji_message_interaction: raw.types.DataJSON = None,
    ) -> bool:
        """Tell the other party that something is happening on your side.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).
                You can also use chat public link in form of *t.me/<username>* (str).

            action (:obj:`~pyrogram.enums.ChatAction`):
                Type of action to broadcast.

            message_thread_id (```int```):
                Unique identifier for the target message thread (topic) of the forum.
                for forum supergroups only.

            business_connection_id (``str``, *optional*):
                Business connection identifier.
                for business bots only.

            emoji (``str``, *optional*):
                The animated emoji. Only supported for :obj:`~pyrogram.enums.ChatAction.TRIGGER_EMOJI_ANIMATION` and :obj:`~pyrogram.enums.ChatAction.WATCH_EMOJI_ANIMATION`.

            emoji_message_id (``int``, *optional*):
                Message identifier of the message containing the animated emoji. Only supported for :obj:`~pyrogram.enums.ChatAction.TRIGGER_EMOJI_ANIMATION`.

            emoji_message_interaction (:obj:`raw.types.DataJSON`, *optional*):
                Only supported for :obj:`~pyrogram.enums.ChatAction.TRIGGER_EMOJI_ANIMATION`.

        Returns:
            ``bool``: On success, True is returned.

        Raises:
            ValueError: In case the provided string is not a valid chat action.

        Example:
            .. code-block:: python

                from pyrogram import enums

                # Send "typing" chat action
                await app.send_chat_action(chat_id, enums.ChatAction.TYPING)

                # Send "upload_video" chat action
                await app.send_chat_action(chat_id, enums.ChatAction.UPLOAD_VIDEO)

                # Send "playing" chat action
                await app.send_chat_action(chat_id, enums.ChatAction.PLAYING)

                # Cancel any current chat action
                await app.send_chat_action(chat_id, enums.ChatAction.CANCEL)
        """

        action_name = action.name.lower()

        if "upload" in action_name or "history" in action_name:
            action = action.value(progress=0)
        elif "watch_emoji" in action_name:
            if emoji is None:
                raise ValueError("Invalid Argument Provided")
            action = action.value(emoticon=emoji)
        elif "trigger_emoji" in action_name:
            if emoji is None or emoji_message_id is None:
                raise ValueError("Invalid Argument Provided")
            if emoji_message_interaction is None:
                _, sticker_set = await self._get_raw_stickers(
                    raw.types.InputStickerSetAnimatedEmojiAnimations(),
                )
                emoji_message_interaction = raw.types.DataJSON(
                    data=dumps(
                        {
                            "v": 1,
                            "a": [
                                {
                                    "t": 0,
                                    "i": randint(1, sticker_set.count),
                                },
                            ],
                        },
                    ),
                )
            action = action.value(
                emoticon=emoji,
                msg_id=emoji_message_id,
                interaction=emoji_message_interaction,
            )
        else:
            action = action.value()
        rpc = raw.functions.messages.SetTyping(
            peer=await self.resolve_peer(chat_id),
            action=action,
            top_msg_id=message_thread_id,
        )
        if business_connection_id:
            return await self.invoke(
                raw.functions.InvokeWithBusinessConnection(
                    connection_id=business_connection_id,
                    query=rpc,
                ),
            )
        return await self.invoke(rpc)
