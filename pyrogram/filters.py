from __future__ import annotations

import inspect
import re
from re import Pattern
from typing import TYPE_CHECKING

import pyrogram
from pyrogram import enums
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineQuery,
    Message,
    PreCheckoutQuery,
    ReplyKeyboardMarkup,
    Story,
    Update,
)

if TYPE_CHECKING:
    from collections.abc import Callable


class Filter:
    async def __call__(self, client: pyrogram.Client, update: Update):
        raise NotImplementedError

    def __invert__(self):
        return InvertFilter(self)

    def __and__(self, other):
        return AndFilter(self, other)

    def __or__(self, other):
        return OrFilter(self, other)


class InvertFilter(Filter):
    def __init__(self, base) -> None:
        self.base = base

    async def __call__(self, client: pyrogram.Client, update: Update):
        if inspect.iscoroutinefunction(self.base.__call__):
            x = await self.base(client, update)
        else:
            x = await client.loop.run_in_executor(
                client.executor,
                self.base,
                client,
                update,
            )

        return not x


class AndFilter(Filter):
    def __init__(self, base, other) -> None:
        self.base = base
        self.other = other

    async def __call__(self, client: pyrogram.Client, update: Update):
        if inspect.iscoroutinefunction(self.base.__call__):
            x = await self.base(client, update)
        else:
            x = await client.loop.run_in_executor(
                client.executor,
                self.base,
                client,
                update,
            )

        if not x:
            return False

        if inspect.iscoroutinefunction(self.other.__call__):
            y = await self.other(client, update)
        else:
            y = await client.loop.run_in_executor(
                client.executor,
                self.other,
                client,
                update,
            )

        return x and y


class OrFilter(Filter):
    def __init__(self, base, other) -> None:
        self.base = base
        self.other = other

    async def __call__(self, client: pyrogram.Client, update: Update):
        if inspect.iscoroutinefunction(self.base.__call__):
            x = await self.base(client, update)
        else:
            x = await client.loop.run_in_executor(
                client.executor,
                self.base,
                client,
                update,
            )

        if x:
            return True

        if inspect.iscoroutinefunction(self.other.__call__):
            y = await self.other(client, update)
        else:
            y = await client.loop.run_in_executor(
                client.executor,
                self.other,
                client,
                update,
            )

        return x or y


CUSTOM_FILTER_NAME = "CustomFilter"


def create(func: Callable, name: str | None = None, **kwargs) -> Filter:
    """Easily create a custom filter.

    Custom filters give you extra control over which updates are allowed or not to be processed by your handlers.

    Parameters:
        func (``Callable``):
            A function that accepts three positional arguments *(filter, client, update)* and returns a boolean: True if the
            update should be handled, False otherwise.
            The *filter* argument refers to the filter itself and can be used to access keyword arguments (read below).
            The *client* argument refers to the :obj:`~pyrogram.Client` that received the update.
            The *update* argument type will vary depending on which `Handler <handlers>`_ is coming from.
            For example, in a :obj:`~pyrogram.handlers.MessageHandler` the *update* argument will be a :obj:`~pyrogram.types.Message`; in a :obj:`~pyrogram.handlers.CallbackQueryHandler` the *update* will be a :obj:`~pyrogram.types.CallbackQuery`.
            Your function body can then access the incoming update attributes and decide whether to allow it or not.

        name (``str``, *optional*):
            Your filter's name. Can be anything you like.
            Defaults to "CustomFilter".

        **kwargs (``any``, *optional*):
            Any keyword argument you would like to pass. Useful when creating parameterized custom filters, such as
            :meth:`~pyrogram.filters.command` or :meth:`~pyrogram.filters.regex`.
    """
    return type(
        name or func.__name__ or CUSTOM_FILTER_NAME,
        (Filter,),
        {"__call__": func, **kwargs},
    )()


async def all_filter(_, __, ___) -> bool:
    return True


all = create(all_filter)
"""Filter all messages."""


async def me_filter(_, __, m: Message):
    return bool(
        (m.from_user and m.from_user.is_self) or getattr(m, "outgoing", False),
    )


me = create(me_filter)
"""Filter messages generated by you yourself."""


async def bot_filter(_, __, m: Message):
    return bool(m.from_user and m.from_user.is_bot)


bot = create(bot_filter)
"""Filter messages coming from bots."""


async def incoming_filter(_, __, m: Message) -> bool:
    return not m.outgoing


incoming = create(incoming_filter)
"""Filter incoming messages. Messages sent to your own chat (Saved Messages) are also recognised as incoming."""


async def outgoing_filter(_, __, m: Message):
    return m.outgoing


outgoing = create(outgoing_filter)
"""Filter outgoing messages. Messages sent to your own chat (Saved Messages) are not recognized as outgoing."""


async def text_filter(_, __, m: Message):
    return bool(m.text)


text = create(text_filter)
"""Filter text messages."""


async def reply_filter(_, __, m: Message):
    return bool(m.reply_to_message_id)


reply = create(reply_filter)
"""Filter messages that are replies to other messages."""


async def reaction_filter(_, __, m: Message):
    return bool(m.edit_hide)


react = create(reaction_filter)
"""Filter reactions."""


async def forwarded_filter(_, __, m: Message):
    return bool(m.forward_date)


forwarded = create(forwarded_filter)
"""Filter messages that are forwarded."""


async def caption_filter(_, __, m: Message):
    return bool(m.caption)


caption = create(caption_filter)
"""Filter media messages that contain captions."""


async def audio_filter(_, __, m: Message):
    return bool(m.audio)


audio = create(audio_filter)
"""Filter messages that contain :obj:`~pyrogram.types.Audio` objects."""


async def document_filter(_, __, m: Message):
    return bool(m.document)


document = create(document_filter)
"""Filter messages that contain :obj:`~pyrogram.types.Document` objects."""


async def photo_filter(_, __, m: Message):
    return bool(m.photo)


photo = create(photo_filter)
"""Filter messages that contain :obj:`~pyrogram.types.Photo` objects."""


async def sticker_filter(_, __, m: Message):
    return bool(m.sticker)


sticker = create(sticker_filter)
"""Filter messages that contain :obj:`~pyrogram.types.Sticker` objects."""


async def animation_filter(_, __, m: Message):
    return bool(m.animation)


animation = create(animation_filter)
"""Filter messages that contain :obj:`~pyrogram.types.Animation` objects."""


async def game_filter(_, __, m: Message):
    return bool(m.game)


game = create(game_filter)
"""Filter messages that contain :obj:`~pyrogram.types.Game` objects."""


async def giveaway_filter(_, __, m: Message):
    return bool(m.giveaway)


giveaway = create(giveaway_filter)
"""Filter messages that contain :obj:`~pyrogram.types.Giveaway` objects."""


async def giveaway_result_filter(_, __, m: Message):
    return bool(m.giveaway_winners or m.giveaway_completed)


giveaway_result = create(giveaway_result_filter)
"""Filter messages that contain :obj:`~pyrogram.types.GiveawayWinners` or :obj:`~pyrogram.types.GiveawayCompleted` objects."""


async def gift_code_filter(_, __, m: Message):
    return bool(m.gift_code)


gift_code = create(gift_code_filter)
"""Filter messages that contain :obj:`~pyrogram.types.GiftCode` objects."""


async def user_gift_filter(_, __, m: Message):
    return bool(m.user_gift)


user_gift = create(user_gift_filter)
"""Filter messages that contain :obj:`~pyrogram.types.UserGift` objects."""


async def video_filter(_, __, m: Message):
    return bool(m.video)


video = create(video_filter)
"""Filter messages that contain :obj:`~pyrogram.types.Video` objects."""


async def media_group_filter(_, __, m: Message):
    return bool(m.media_group_id)


media_group = create(media_group_filter)
"""Filter messages containing photos or videos being part of an album."""


async def voice_filter(_, __, m: Message):
    return bool(m.voice)


voice = create(voice_filter)
"""Filter messages that contain :obj:`~pyrogram.types.Voice` note objects."""


async def video_note_filter(_, __, m: Message):
    return bool(m.video_note)


video_note = create(video_note_filter)
"""Filter messages that contain :obj:`~pyrogram.types.VideoNote` objects."""


async def contact_filter(_, __, m: Message):
    return bool(m.contact)


contact = create(contact_filter)
"""Filter messages that contain :obj:`~pyrogram.types.Contact` objects."""


async def location_filter(_, __, m: Message):
    return bool(m.location)


location = create(location_filter)
"""Filter messages that contain :obj:`~pyrogram.types.Location` objects."""


async def venue_filter(_, __, m: Message):
    return bool(m.venue)


venue = create(venue_filter)
"""Filter messages that contain :obj:`~pyrogram.types.Venue` objects."""


async def web_page_filter(_, __, m: Message):
    return bool(m.web_page)


web_page = create(web_page_filter)
"""Filter messages sent with a webpage preview."""


async def poll_filter(_, __, m: Message):
    return bool(m.poll)


poll = create(poll_filter)
"""Filter messages that contain :obj:`~pyrogram.types.Poll` objects."""


async def dice_filter(_, __, m: Message):
    return bool(m.dice)


dice = create(dice_filter)
"""Filter messages that contain :obj:`~pyrogram.types.Dice` objects."""


async def media_spoiler_filter(_, __, m: Message):
    return bool(m.has_media_spoiler)


media_spoiler = create(media_spoiler_filter)
"""Filter media messages that contain a spoiler."""


async def private_filter(_, __, m: Message):
    return bool(
        m.chat and m.chat.type in {enums.ChatType.PRIVATE, enums.ChatType.BOT},
    )


private = create(private_filter)
"""Filter messages sent in private chats."""


async def group_filter(_, __, m: Message):
    return bool(
        m.chat and m.chat.type in {enums.ChatType.GROUP, enums.ChatType.SUPERGROUP},
    )


group = create(group_filter)
"""Filter messages sent in group or supergroup chats."""


async def channel_filter(_, __, m: Message):
    return bool(m.chat and m.chat.type == enums.ChatType.CHANNEL)


channel = create(channel_filter)
"""Filter messages sent in channels."""


async def new_chat_members_filter(_, __, m: Message):
    return bool(m.new_chat_members)


new_chat_members = create(new_chat_members_filter)
"""Filter service messages for new chat members."""


async def left_chat_member_filter(_, __, m: Message):
    return bool(m.left_chat_member)


left_chat_member = create(left_chat_member_filter)
"""Filter service messages for members that left the chat."""


async def new_chat_title_filter(_, __, m: Message):
    return bool(m.new_chat_title)


new_chat_title = create(new_chat_title_filter)
"""Filter service messages for new chat titles."""


async def new_chat_photo_filter(_, __, m: Message):
    return bool(m.new_chat_photo)


new_chat_photo = create(new_chat_photo_filter)
"""Filter service messages for new chat photos."""


async def delete_chat_photo_filter(_, __, m: Message):
    return bool(m.delete_chat_photo)


delete_chat_photo = create(delete_chat_photo_filter)
"""Filter service messages for deleted photos."""


async def group_chat_created_filter(_, __, m: Message):
    return bool(m.group_chat_created)


group_chat_created = create(group_chat_created_filter)
"""Filter service messages for group chat creations."""


async def supergroup_chat_created_filter(_, __, m: Message):
    return bool(m.supergroup_chat_created)


supergroup_chat_created = create(supergroup_chat_created_filter)
"""Filter service messages for supergroup chat creations."""


async def channel_chat_created_filter(_, __, m: Message):
    return bool(m.channel_chat_created)


channel_chat_created = create(channel_chat_created_filter)
"""Filter service messages for channel chat creations."""


async def migrate_to_chat_id_filter(_, __, m: Message):
    return bool(m.migrate_to_chat_id)


migrate_to_chat_id = create(migrate_to_chat_id_filter)
"""Filter service messages that contain migrate_to_chat_id."""


async def migrate_from_chat_id_filter(_, __, m: Message):
    return bool(m.migrate_from_chat_id)


migrate_from_chat_id = create(migrate_from_chat_id_filter)
"""Filter service messages that contain migrate_from_chat_id."""


async def pinned_message_filter(_, __, m: Message):
    return bool(m.pinned_message)


pinned_message = create(pinned_message_filter)
"""Filter service messages for pinned messages."""


async def game_high_score_filter(_, __, m: Message):
    return bool(m.game_high_score)


game_high_score = create(game_high_score_filter)
"""Filter service messages for game high scores."""


async def reply_keyboard_filter(_, __, m: Message):
    return isinstance(m.reply_markup, ReplyKeyboardMarkup)


reply_keyboard = create(reply_keyboard_filter)
"""Filter messages containing reply keyboard markups"""


async def inline_keyboard_filter(_, __, m: Message):
    return isinstance(m.reply_markup, InlineKeyboardMarkup)


inline_keyboard = create(inline_keyboard_filter)
"""Filter messages containing inline keyboard markups"""


async def mentioned_filter(_, __, m: Message):
    return bool(m.mentioned)


mentioned = create(mentioned_filter)
"""Filter messages containing mentions"""


async def via_bot_filter(_, __, m: Message):
    return bool(m.via_bot)


via_bot = create(via_bot_filter)
"""Filter messages sent via inline bots"""


async def video_chat_started_filter(_, __, m: Message):
    return bool(m.video_chat_started)


video_chat_started = create(video_chat_started_filter)
"""Filter messages for started video chats"""


async def video_chat_ended_filter(_, __, m: Message):
    return bool(m.video_chat_ended)


video_chat_ended = create(video_chat_ended_filter)
"""Filter messages for ended video chats"""


async def video_chat_members_invited_filter(_, __, m: Message):
    return bool(m.video_chat_members_invited)


video_chat_members_invited = create(video_chat_members_invited_filter)
"""Filter messages for voice chat invited members"""


async def successful_payment_filter(_, __, m: Message):
    return bool(m.successful_payment)


successful_payment = create(successful_payment_filter)
"""Filter messages for successful payments"""


async def service_filter(_, __, m: Message):
    return bool(m.service)


service = create(service_filter)
"""Filter service messages.

A service message contains any of the following fields set: *left_chat_member*,
*new_chat_title*, *new_chat_photo*, *delete_chat_photo*, *group_chat_created*, *supergroup_chat_created*,
*channel_chat_created*, *migrate_to_chat_id*, *migrate_from_chat_id*, *pinned_message*, *game_score*,
*video_chat_started*, *video_chat_ended*, *video_chat_members_invited*, *successful_payment*, *successful_payment*.
"""


async def media_filter(_, __, m: Message):
    return bool(m.media)


media = create(media_filter)
"""Filter media messages.

A media message contains any of the following fields set: *audio*, *document*, *photo*, *sticker*, *video*,
*animation*, *voice*, *video_note*, *contact*, *location*, *venue*, *poll*.
"""


async def scheduled_filter(_, __, m: Message):
    return bool(m.scheduled)


scheduled = create(scheduled_filter)
"""Filter messages that have been scheduled (not yet sent)."""


async def from_scheduled_filter(_, __, m: Message):
    return bool(m.from_scheduled)


from_scheduled = create(from_scheduled_filter)
"""Filter new automatically sent messages that were previously scheduled."""


async def linked_channel_filter(_, __, m: Message):
    return bool(m.forward_from_chat and not m.from_user)


linked_channel = create(linked_channel_filter)
"""Filter messages that are automatically forwarded from the linked channel to the group chat."""


async def forum_topic_closed_filter(_, __, m: Message):
    return bool(m.forum_topic_closed)


forum_topic_closed = create(forum_topic_closed_filter)
"""Filter service message for closed forum topics"""


async def forum_topic_created_filter(_, __, m: Message):
    return bool(m.forum_topic_created)


forum_topic_created = create(forum_topic_created_filter)
"""Filter service message for created forum topics"""


async def forum_topic_edited_filter(_, __, m: Message):
    return bool(m.forum_topic_edited)


forum_topic_edited = create(forum_topic_edited_filter)
"""Filter service message for edited forum topics"""


async def forum_topic_reopened_filter(_, __, m: Message):
    return bool(m.forum_topic_reopened)


forum_topic_reopened = create(forum_topic_reopened_filter)
"""Filter service message for reopened forum topics"""


async def general_topic_hidden_filter(_, __, m: Message):
    return bool(m.general_topic_hidden)


general_forum_topic_hidden = create(general_topic_hidden_filter)

"""Filter service message for hidden general forum topics"""


async def general_topic_unhidden_filter(_, __, m: Message):
    return bool(m.general_topic_unhidden)


general_forum_topic_unhidden = create(general_topic_unhidden_filter)
"""Filter service message for unhidden general forum topics"""


def command(
    commands: str | list[str],
    prefixes: str | list[str] = "/",
    case_sensitive: bool = False,
):
    """Filter commands, i.e.: text messages starting with "/" or any other custom prefix.

    Parameters:
        commands (``str`` | ``list``):
            The command or list of commands as string the filter should look for.
            Examples: "start", ["start", "help", "settings"]. When a message text containing
            a command arrives, the command itself and its arguments will be stored in the *command*
            field of the :obj:`~pyrogram.types.Message`.

        prefixes (``str`` | ``list``, *optional*):
            A prefix or a list of prefixes as string the filter should look for.
            Defaults to "/" (slash). Examples: ".", "!", ["/", "!", "."], list(".:!").
            Pass None or "" (empty string) to allow commands with no prefix at all.

        case_sensitive (``bool``, *optional*):
            Pass True if you want your command(s) to be case sensitive. Defaults to False.
            Examples: when True, command="Start" would trigger /Start but not /start.
    """
    command_re = re.compile(r"([\"'])(.*?)(?<!\\)\1|(\S+)")

    async def func(flt, client: pyrogram.Client, message: Message) -> bool:
        username = client.me.username or ""
        text = message.text or message.caption
        message.command = None

        if not text:
            return False

        for prefix in flt.prefixes:
            if not text.startswith(prefix):
                continue

            without_prefix = text[len(prefix) :]

            for cmd in flt.commands:
                if not re.match(
                    rf"^(?:{cmd}(?:@?{username})?)(?:\s|$)",
                    without_prefix,
                    flags=re.IGNORECASE if not flt.case_sensitive else 0,
                ):
                    continue

                without_command = re.sub(
                    rf"{cmd}(?:@?{username})?\s?",
                    "",
                    without_prefix,
                    count=1,
                    flags=re.IGNORECASE if not flt.case_sensitive else 0,
                )

                message.command = [cmd] + [
                    re.sub(
                        r"\\([\"'])",
                        r"\1",
                        m.group(2) or m.group(3) or "",
                    )
                    for m in command_re.finditer(without_command)
                ]

                return True

        return False

    commands = commands if isinstance(commands, list) else [commands]
    commands = {c if case_sensitive else c.lower() for c in commands}

    prefixes = [] if prefixes is None else prefixes
    prefixes = prefixes if isinstance(prefixes, list) else [prefixes]
    prefixes = set(prefixes) if prefixes else {""}

    return create(
        func,
        "CommandFilter",
        commands=commands,
        prefixes=prefixes,
        case_sensitive=case_sensitive,
    )


def regex(pattern: str | Pattern, flags: int = 0):
    """Filter updates that match a given regular expression pattern.

    Can be applied to handlers that receive one of the following updates:

    - :obj:`~pyrogram.types.Message`: The filter will match ``text`` or ``caption``.
    - :obj:`~pyrogram.types.CallbackQuery`: The filter will match ``data``.
    - :obj:`~pyrogram.types.InlineQuery`: The filter will match ``query``.
    - :obj:`~pyrogram.types.PreCheckoutQuery`: The filter will match ``payload``.

    When a pattern matches, all the `Match Objects <https://docs.python.org/3/library/re.html#match-objects>`_ are
    stored in the ``matches`` field of the update object itself.

    Parameters:
        pattern (``str`` | ``Pattern``):
            The regex pattern as string or as pre-compiled pattern.

        flags (``int``, *optional*):
            Regex flags.
    """

    async def func(flt, _, update: Update):
        if isinstance(update, Message):
            value = update.text or update.caption
        elif isinstance(update, CallbackQuery):
            value = update.data
        elif isinstance(update, InlineQuery):
            value = update.query
        elif isinstance(update, PreCheckoutQuery):
            value = update.payload
        else:
            raise ValueError(f"Regex filter doesn't work with {type(update)}")

        if value:
            update.matches = list(flt.p.finditer(value)) or None

        return bool(update.matches)

    return create(
        func,
        "RegexFilter",
        p=pattern if isinstance(pattern, Pattern) else re.compile(pattern, flags),
    )


class user(Filter, set):
    """Filter messages coming from one or more users.

    You can use `set bound methods <https://docs.python.org/3/library/stdtypes.html#set>`_ to manipulate the
    users container.

    Parameters:
        users (``int`` | ``str`` | ``list``):
            Pass one or more user ids/usernames to filter users.
            For you yourself, "me" or "self" can be used as well.
            Defaults to None (no users).
    """

    def __init__(self, users: int | str | list[int | str] | None = None) -> None:
        users = (
            [] if users is None else users if isinstance(users, list) else [users]
        )

        super().__init__(
            "me"
            if u in ["me", "self"]
            else u.lower().strip("@")
            if isinstance(u, str)
            else u
            for u in users
        )

    async def __call__(self, _, message: Message):
        return message.from_user and (
            message.from_user.id in self
            or (
                message.from_user.username
                and message.from_user.username.lower() in self
            )
            or ("me" in self and message.from_user.is_self)
        )


class chat(Filter, set):
    """Filter messages coming from one or more chats.

    You can use `set bound methods <https://docs.python.org/3/library/stdtypes.html#set>`_ to manipulate the
    chats container.

    Parameters:
        chats (``int`` | ``str`` | ``list``):
            Pass one or more chat ids/usernames to filter chats.
            For your personal cloud (Saved Messages) you can simply use "me" or "self".
            Defaults to None (no chats).
    """

    def __init__(self, chats: int | str | list[int | str] | None = None) -> None:
        chats = (
            [] if chats is None else chats if isinstance(chats, list) else [chats]
        )

        super().__init__(
            "me"
            if c in ["me", "self"]
            else c.lower().strip("@")
            if isinstance(c, str)
            else c
            for c in chats
        )

    async def __call__(self, _, message: Message | Story):
        if isinstance(message, Story):
            return (
                message.sender_chat
                and (
                    message.sender_chat.id in self
                    or (
                        message.sender_chat.username
                        and message.sender_chat.username.lower() in self
                    )
                )
            ) or (
                message.from_user
                and (
                    message.from_user.id in self
                    or (
                        message.from_user.username
                        and message.from_user.username.lower() in self
                    )
                )
            )
        return message.chat and (
            message.chat.id in self
            or (message.chat.username and message.chat.username.lower() in self)
            or (
                "me" in self
                and message.from_user
                and message.from_user.is_self
                and not message.outgoing
            )
        )


class topic(Filter, set):
    """Filter messages coming from one or more topics.
    You can use `set bound methods <https://docs.python.org/3/library/stdtypes.html#set>`_ to manipulate the
    topics container.
    Parameters:
        topics (``int`` | ``list``):
            Pass one or more topic ids to filter messages in specific topics.
            Defaults to None (no topics).
    """

    def __init__(self, topics: int | list[int] | None = None) -> None:
        topics = (
            []
            if topics is None
            else topics
            if isinstance(topics, list)
            else [topics]
        )

        super().__init__(t for t in topics)

    async def __call__(self, _, message: Message):
        return message.topic and message.topic.id in self
