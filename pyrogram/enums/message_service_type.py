from __future__ import annotations

from enum import auto

from .auto_name import AutoName


class MessageServiceType(AutoName):
    """Message service type enumeration used in :obj:`~pyrogram.types.Message`."""

    NEW_CHAT_MEMBERS = auto()
    "New members join"

    LEFT_CHAT_MEMBERS = auto()
    "Left chat members"

    NEW_CHAT_TITLE = auto()
    "New chat title"

    NEW_CHAT_PHOTO = auto()
    "New chat photo"

    DELETE_CHAT_PHOTO = auto()
    "Deleted chat photo"

    GROUP_CHAT_CREATED = auto()
    "Group chat created"

    CHANNEL_CHAT_CREATED = auto()
    "Channel chat created"

    MIGRATE_TO_CHAT_ID = auto()
    "Migrated to chat id"

    MIGRATE_FROM_CHAT_ID = auto()
    "Migrated from chat id"

    PINNED_MESSAGE = auto()
    "Pinned message"

    GAME_HIGH_SCORE = auto()
    "Game high score"

    ChatShared = auto()
    "a shared chat/channel/user"

    FORUM_TOPIC_CREATED = auto()
    "a new forum topic created in the chat"

    FORUM_TOPIC_CLOSED = auto()
    "a new forum topic closed in the chat"

    FORUM_TOPIC_REOPENED = auto()
    "a new forum topic reopened in the chat"

    FORUM_TOPIC_EDITED = auto()
    "a new forum topic renamed in the chat"

    GENERAL_TOPIC_HIDDEN = auto()
    "a forum general topic hidden in the chat"

    GENERAL_TOPIC_UNHIDDEN = auto()
    "a forum general topic unhidden in the chat"

    VIDEO_CHAT_STARTED = auto()
    "Video chat started"

    VIDEO_CHAT_ENDED = auto()
    "Video chat ended"

    VIDEO_CHAT_SCHEDULED = auto()
    "Video chat scheduled"

    VIDEO_CHAT_MEMBERS_INVITED = auto()
    "Video chat members invited"

    WEB_APP_DATA = auto()
    "Web app data"

    GIFTED_PREMIUM = auto()
    "Gifted Premium"

    USER_GIFT = auto()
    "Star gift"

    STAR_GIFT = auto()
    "Star gift"

    GIVEAWAY_LAUNCHED = auto()
    "Giveaway Launch"

    GIVEAWAY_RESULT = auto()
    "Giveaway Result"

    BOOST_APPLY = auto()
    "Boost apply"

    SUCCESSFUL_PAYMENT = auto()
    "Successful payment"

    PAYMENT_REFUNDED = auto()
    "Payment refunded"

    BOT_ALLOWED = auto()
    "Bot allowed"

    CONTACT_REGISTERED = auto()
    "A contact has registered with Telegram"

    SCREENSHOT_TAKEN = auto()
    "A screenshot of a message in the chat has been taken"

    UNKNOWN = auto()
    "This service message is unsupported by the current version of Electrogram"
