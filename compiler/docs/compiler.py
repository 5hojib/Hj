from __future__ import annotations

import ast
import os
import re
import shutil
from pathlib import Path

HOME = "compiler/docs"
DESTINATION = "docs/source/telegram"
PYROGRAM_API_DEST = "docs/source/api"

FUNCTIONS_PATH = "pyrogram/raw/functions"
TYPES_PATH = "pyrogram/raw/types"
BASE_PATH = "pyrogram/raw/base"

FUNCTIONS_BASE = "functions"
TYPES_BASE = "types"
BASE_BASE = "base"


def snake(s: str):
    s = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", s)
    return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s).lower()


def generate(source_path, base) -> None:
    all_entities = {}

    def build(path, level=0) -> None:
        last = path.split("/")[-1]

        for i in os.listdir(path):
            try:
                if not i.startswith("__"):
                    build("/".join([path, i]), level=level + 1)
            except NotADirectoryError:
                with Path(path, i).open(encoding="utf-8") as f:
                    p = ast.parse(f.read())

                for node in ast.walk(p):
                    if isinstance(node, ast.ClassDef):
                        name = node.name
                        break
                else:
                    continue

                full_path = (
                    Path(path).name + "/" + snake(name).replace("_", "-") + ".rst"
                )

                if level:
                    full_path = base + "/" + full_path

                namespace = path.split("/")[-1]
                if namespace in ["base", "types", "functions"]:
                    namespace = ""

                full_name = f"{(namespace + '.') if namespace else ''}{name}"

                Path(DESTINATION, full_path).parent.mkdir(
                    parents=True, exist_ok=True
                )

                with Path(DESTINATION, full_path).open("w", encoding="utf-8") as f:
                    f.write(
                        page_template.format(
                            title=full_name,
                            title_markup="=" * len(full_name),
                            full_class_path="pyrogram.raw.{}".format(
                                ".".join(full_path.split("/")[:-1]) + "." + name
                            ),
                        )
                    )

                if last not in all_entities:
                    all_entities[last] = []

                all_entities[last].append(name)

    build(source_path)

    for k, v in sorted(all_entities.items()):
        v = sorted(v)
        entities = [f'{i} <{snake(i).replace("_", "-")}>' for i in v]

        if k != base:
            inner_path = base + "/" + k + "/index" + ".rst"
            module = f"pyrogram.raw.{base}.{k}"
        else:
            for i in sorted(all_entities, reverse=True):
                if i != base:
                    entities.insert(0, f"{i}/index")

            inner_path = base + "/index" + ".rst"
            module = f"pyrogram.raw.{base}"

        with Path(DESTINATION, inner_path).open("w", encoding="utf-8") as f:
            if k == base:
                f.write(":tocdepth: 1\n\n")
                k = "Raw " + k

            f.write(
                toctree.format(
                    title=k.title(),
                    title_markup="=" * len(k),
                    module=module,
                    entities="\n    ".join(entities),
                )
            )

            f.write("\n")


def pyrogram_api() -> None:
    def get_title_list(s: str) -> list:
        return [i.strip() for i in [j.strip() for j in s.split("\n") if j] if i]

    # Methods

    categories = {
        "utilities": """
        Utilities
            start
            stop
            run
            run_sync
            restart
            add_handler
            remove_handler
            stop_transmission
            export_session_string
            set_parse_mode
        """,
        "messages": """
        Messages
            send_message
            forward_messages
            copy_message
            copy_media_group
            send_photo
            send_audio
            send_document
            send_sticker
            send_video
            send_animation
            send_voice
            send_video_note
            send_web_page
            send_media_group
            send_location
            send_venue
            send_contact
            send_cached_media
            send_reaction
            send_paid_reaction
            send_paid_media
            edit_message_text
            edit_message_caption
            edit_message_media
            edit_message_reply_markup
            edit_inline_text
            edit_inline_caption
            edit_inline_media
            edit_inline_reply_markup
            send_chat_action
            delete_messages
            delete_scheduled_messages
            get_available_effects
            get_messages
            get_scheduled_messages
            get_media_group
            get_chat_history
            get_chat_history_count
            read_chat_history
            send_poll
            vote_poll
            stop_poll
            retract_vote
            send_dice
            search_messages
            search_messages_count
            search_global
            search_global_count
            search_global_hashtag_messages
            search_global_hashtag_messages_count
            download_media
            stream_media
            get_discussion_message
            get_discussion_replies
            get_discussion_replies_count
            get_custom_emoji_stickers
            translate_text
        """,
        "chats": """
        Chats
            join_chat
            leave_chat
            ban_chat_member
            unban_chat_member
            restrict_chat_member
            promote_chat_member
            set_administrator_title
            set_chat_photo
            delete_chat_photo
            delete_folder
            export_folder_link
            set_chat_title
            set_chat_description
            set_chat_permissions
            pin_chat_message
            unpin_chat_message
            unpin_all_chat_messages
            get_chat
            get_chat_member
            get_chat_members
            get_chat_members_count
            get_dialogs
            get_dialogs_count
            get_folders
            get_forum_topics
            get_forum_topics_by_id
            set_chat_username
            archive_chats
            unarchive_chats
            add_chat_members
            create_channel
            create_group
            create_supergroup
            delete_channel
            delete_supergroup
            delete_user_history
            set_slow_mode
            mark_chat_unread
            get_chat_event_log
            get_chat_online_count
            get_send_as_chats
            set_send_as_chat
            set_chat_protected_content
            close_forum_topic
            close_general_topic
            create_forum_topic
            delete_forum_topic
            edit_forum_topic
            edit_general_topic
            hide_general_topic
            reopen_forum_topic
            reopen_general_topic
            unhide_general_topic
            update_color
            delete_chat_history
            update_folder
        """,
        "users": """
        Users
            delete_account
            get_me
            get_users
            get_chat_photos
            get_chat_photos_count
            set_profile_photo
            delete_profile_photos
            set_username
            update_birthday
            update_personal_chat
            update_profile
            block_user
            unblock_user
            get_common_chats
            get_default_emoji_statuses
            set_emoji_status
        """,
        "stories": """
        Stories
            delete_stories
            edit_story
            export_story_link
            forward_story
            get_all_stories
            get_stories
            get_stories_history
            get_peer_stories
            send_story
        """,
        "stickers": """
        Stickers
            add_sticker_to_set
            create_sticker_set
            get_sticker_set
        """,
        "invite_links": """
        Invite Links
            get_chat_invite_link
            export_chat_invite_link
            create_chat_invite_link
            edit_chat_invite_link
            revoke_chat_invite_link
            delete_chat_invite_link
            get_chat_invite_link_joiners
            get_chat_invite_link_joiners_count
            get_chat_admin_invite_links
            get_chat_admin_invite_links_count
            get_chat_admins_with_invite_links
            get_chat_join_requests
            delete_chat_admin_invite_links
            approve_chat_join_request
            approve_all_chat_join_requests
            decline_chat_join_request
            decline_all_chat_join_requests
        """,
        "contacts": """
        Contacts
            add_contact
            delete_contacts
            import_contacts
            get_contacts
            get_contacts_count
            search_contacts
        """,
        "password": """
        Password
            enable_cloud_password
            change_cloud_password
            remove_cloud_password
        """,
        "bots": """
        Bots
            get_inline_bot_results
            send_inline_bot_result
            answer_callback_query
            answer_inline_query
            request_callback_answer
            send_game
            set_game_score
            get_game_high_scores
            set_bot_commands
            get_bot_commands
            delete_bot_commands
            set_bot_default_privileges
            get_bot_default_privileges
            set_chat_menu_button
            get_chat_menu_button
            answer_web_app_query
            get_bot_info
            set_bot_info
            get_collectible_item_info
        """,
        "business": """
        Telegram Business
            answer_pre_checkout_query
            answer_shipping_query
            create_invoice_link
            get_business_connection
            get_stars_transactions
            get_stars_transactions_by_id
            refund_star_payment
            send_invoice
            get_payment_form
            send_payment_form
        """,
        "authorization": """
        Authorization
            connect
            disconnect
            initialize
            terminate
            send_code
            resend_code
            sign_in
            sign_in_bot
            sign_up
            get_password_hint
            check_password
            send_recovery_code
            recover_password
            accept_terms_of_service
            log_out
            get_active_sessions
            reset_session
            reset_sessions
        """,
        "advanced": """
        Advanced
            invoke
            resolve_peer
            save_file
        """,
        "account": """
        Account
            get_account_ttl
            set_account_ttl
            set_privacy
            get_privacy
        """,
    }

    root = PYROGRAM_API_DEST + "/methods"

    shutil.rmtree(root, ignore_errors=True)
    Path(root).mkdir()

    with Path(HOME, "template/methods.rst").open() as f:
        template = f.read()

    with Path(root, "index.rst").open("w") as f:
        fmt_keys = {}

        for k, v in categories.items():
            name, *methods = get_title_list(v)
            fmt_keys.update({k: "\n    ".join(f"{m} <{m}>" for m in methods)})

            for method in methods:
                with Path(root, f"{method}.rst").open("w") as f2:
                    title = f"{method}()"

                    f2.write(title + "\n" + "=" * len(title) + "\n\n")
                    f2.write(f".. automethod:: pyrogram.Client.{method}()")

            functions = ["idle", "compose"]

            for func in functions:
                with Path(root, f"{func}.rst").open("w") as f2:
                    title = f"{func}()"

                    f2.write(title + "\n" + "=" * len(title) + "\n\n")
                    f2.write(f".. autofunction:: pyrogram.{func}()")

        f.write(template.format(**fmt_keys))

    # Types

    categories = {
        "users_chats": """
        Users & Chats
            Birthday
            BusinessInfo
            BusinessMessage
            BusinessRecipients
            BusinessWeeklyOpen
            BusinessWorkingHours
            User
            Chat
            ChatPreview
            ChatPhoto
            ChatMember
            ChatPermissions
            ChatPrivileges
            ChatInviteLink
            ChatAdminWithInviteLinks
            ChatEvent
            ChatEventFilter
            ChatMemberUpdated
            ChatJoinRequest
            ChatJoinedByRequest
            ChatJoiner
            Dialog
            Folder
            Restriction
            EmojiStatus
            ForumTopic
            PeerUser
            PeerChannel
            BotInfo
            ChatColor
            FoundContacts
            PrivacyRule
            CollectibleItemInfo
        """,
        "messages_media": """
        Messages & Media
            Message
            MessageEntity
            Photo
            Thumbnail
            Audio
            AvailableEffect
            Document
            Animation
            LabeledPrice
            Video
            Voice
            VideoNote
            Contact
            Location
            Venue
            Sticker
            StickerSet
            ContactRegistered
            ScreenshotTaken
            Game
            GiftedPremium
            Giveaway
            GiveawayLaunched
            GiveawayResult
            MessageStory
            WebPage
            WebPageEmpty
            WebPagePreview
            Poll
            PollOption
            Dice
            VideoChatScheduled
            VideoChatStarted
            VideoChatEnded
            VideoChatMembersInvited
            WebAppData
            MessageReactions
            MessageReactor
            ChatReactions
            ForumTopicCreated
            ForumTopicEdited
            ForumTopicClosed
            ForumTopicReopened
            GeneralTopicHidden
            GeneralTopicUnhidden
            Reaction
            ReactionTypePaid
            ReactionCount
            ReactionType
            MessageReactionUpdated
            MessageReactionCountUpdated
            TranslatedText
            DraftMessage
        """,
        "stories": """
        Stories
            Story
            StoryDeleted
            StoryForwardHeader
            StorySkipped
            StoriesPrivacyRules
            StoryViews
            MediaArea
            MediaAreaChannelPost
            MediaAreaCoordinates
            InputMediaArea
            InputMediaAreaChannelPost
        """,
        "bot": """
        Bot
            BotAllowed
            BotApp
            BotBusinessConnection
        """,
        "bot_keyboards": """
        Bot keyboards
            ReplyKeyboardMarkup
            KeyboardButton
            ReplyKeyboardRemove
            InlineKeyboardMarkup
            InlineKeyboardButton
            InlineKeyboardButtonBuy
            RequestPeerTypeChannel
            RequestPeerTypeChat
            RequestPeerTypeUser
            RequestedChats
            RequestedChat
            RequestedUser
            LoginUrl
            ForceReply
            CallbackQuery
            GameHighScore
            CallbackGame
            WebAppInfo
            MenuButton
            MenuButtonCommands
            MenuButtonWebApp
            MenuButtonDefault
            SentWebAppMessage
            PreCheckoutQuery
        """,
        "bot_commands": """
        Bot commands
            BotCommand
            BotCommandScope
            BotCommandScopeDefault
            BotCommandScopeAllPrivateChats
            BotCommandScopeAllGroupChats
            BotCommandScopeAllChatAdministrators
            BotCommandScopeChat
            BotCommandScopeChatAdministrators
            BotCommandScopeChatMember
        """,
        "business": """
        Telegram Business
            ExtendedMediaPreview
            InputStarsTransaction
            Invoice
            PaidMedia
            PaidMediaPreview
            PaymentForm
            PaymentInfo
            PaymentRefunded
            ShippingAddress
            ShippingOption
            ShippingQuery
            StarsStatus
            StarsTransaction
            SuccessfulPayment
        """,
        "input_media": """
        Input Media
            InputMedia
            InputMediaPhoto
            InputMediaVideo
            InputMediaAudio
            InputMediaAnimation
            InputMediaDocument
            InputPhoneContact
        """,
        "inline_mode": """
        Inline Mode
            InlineQuery
            InlineQueryResult
            InlineQueryResultCachedAudio
            InlineQueryResultCachedDocument
            InlineQueryResultCachedAnimation
            InlineQueryResultCachedPhoto
            InlineQueryResultCachedSticker
            InlineQueryResultCachedVideo
            InlineQueryResultCachedVoice
            InlineQueryResultArticle
            InlineQueryResultAudio
            InlineQueryResultContact
            InlineQueryResultDocument
            InlineQueryResultAnimation
            InlineQueryResultLocation
            InlineQueryResultPhoto
            InlineQueryResultVenue
            InlineQueryResultVideo
            InlineQueryResultVoice
            ChosenInlineResult
        """,
        "pre_checkout_query": """
        PreCheckoutQuery
            PreCheckoutQuery.answer
        """,
        "shipping_query": """
        ShippingQuery
            ShippingQuery.answer
        """,
        "input_message_content": """
        InputMessageContent
            InputMessageContent
            InputReplyToMessage
            InputReplyToStory
            InputTextMessageContent
            InputLocationMessageContent
            InputVenueMessageContent
            InputContactMessageContent
            InputInvoiceMessageContent
        """,
        "authorization": """
        Authorization
            ActiveSession
            ActiveSessions
            SentCode
            TermsOfService
        """,
        "input_privacy_rule": """
        InputPrivacyRule
            InputPrivacyRuleAllowAll
            InputPrivacyRuleAllowContacts
            InputPrivacyRuleAllowPremium
            InputPrivacyRuleAllowUsers
            InputPrivacyRuleAllowChats
            InputPrivacyRuleDisallowAll
            InputPrivacyRuleDisallowContacts
            InputPrivacyRuleDisallowUsers
            InputPrivacyRuleDisallowChats
        """,
    }

    root = PYROGRAM_API_DEST + "/types"

    shutil.rmtree(root, ignore_errors=True)
    Path(root).mkdir()

    with Path(HOME, "template/types.rst").open() as f:
        template = f.read()

    with Path(root, "index.rst").open("w") as f:
        fmt_keys = {}

        for k, v in categories.items():
            name, *types = get_title_list(v)

            fmt_keys.update({k: "\n    ".join(types)})

            for type in types:
                with Path(root, f"{type}.rst").open("w") as f2:
                    title = f"{type}"

                    f2.write(title + "\n" + "=" * len(title) + "\n\n")
                    f2.write(f".. autoclass:: pyrogram.types.{type}()\n")

        f.write(template.format(**fmt_keys))

    # Bound Methods

    categories = {
        "message": """
        Message
            Message.ask
            Message.click
            Message.delete
            Message.download
            Message.forward
            Message.copy
            Message.pin
            Message.unpin
            Message.edit
            Message.edit_text
            Message.edit_caption
            Message.edit_media
            Message.edit_reply_markup
            Message.reply
            Message.reply_text
            Message.reply_animation
            Message.reply_audio
            Message.reply_cached_media
            Message.reply_chat_action
            Message.reply_contact
            Message.reply_document
            Message.reply_game
            Message.reply_inline_bot_result
            Message.reply_location
            Message.reply_media_group
            Message.reply_photo
            Message.reply_poll
            Message.reply_sticker
            Message.reply_venue
            Message.reply_video
            Message.reply_video_note
            Message.reply_voice
            Message.reply_web_page
            Message.get_media_group
            Message.react
            Message.wait_for_click
            Message.pay
        """,
        "chat": """
        Chat
            Chat.ask
            Chat.listen
            Chat.stop_listening
            Chat.archive
            Chat.unarchive
            Chat.set_title
            Chat.set_description
            Chat.set_photo
            Chat.ban_member
            Chat.unban_member
            Chat.restrict_member
            Chat.promote_member
            Chat.get_member
            Chat.get_members
            Chat.add_members
            Chat.join
            Chat.leave
            Chat.mark_unread
            Chat.set_protected_content
            Chat.unpin_all_messages
        """,
        "user": """
        User
            User.ask
            User.listen
            User.stop_listening
            User.archive
            User.unarchive
            User.block
            User.unblock
        """,
        "story": """
        Story
            Story.delete
            Story.download
            Story.react
            Story.edit
            Story.edit_animation
            Story.edit_caption
            Story.edit_photo
            Story.edit_privacy
            Story.edit_video
            Story.export_link
            Story.forward
            Story.reply_text
            Story.reply_animation
            Story.reply_audio
            Story.reply_cached_media
            Story.reply_media_group
            Story.reply_photo
            Story.reply_sticker
            Story.reply_video
            Story.reply_video_note
            Story.reply_voice
        """,
        "callback_query": """
        Callback Query
            CallbackQuery.answer
            CallbackQuery.edit_message_text
            CallbackQuery.edit_message_caption
            CallbackQuery.edit_message_media
            CallbackQuery.edit_message_reply_markup
        """,
        "inline_query": """
        InlineQuery
            InlineQuery.answer
        """,
        "pre_checkout_query": """
        PreCheckoutQuery
            PreCheckoutQuery.answer
        """,
        "shipping_query": """
        ShippingQuery
            ShippingQuery.answer
        """,
        "chat_join_request": """
        ChatJoinRequest
            ChatJoinRequest.approve
            ChatJoinRequest.decline
        """,
        "active_session": """
        ActiveSession
            ActiveSession.reset
        """,
    }

    root = PYROGRAM_API_DEST + "/bound-methods"

    shutil.rmtree(root, ignore_errors=True)
    Path(root).mkdir()

    with Path(HOME, "template/bound-methods.rst").open() as f:
        template = f.read()

    with Path(root, "index.rst").open("w") as f:
        fmt_keys = {}

        for k, v in categories.items():
            name, *bound_methods = get_title_list(v)

            fmt_keys.update(
                {
                    f"{k}_hlist": "\n    ".join(
                        f"- :meth:`~{bm}`" for bm in bound_methods
                    )
                }
            )

            fmt_keys.update(
                {
                    f"{k}_toctree": "\n    ".join(
                        "{} <{}>".format(bm.split(".")[1], bm)
                        for bm in bound_methods
                    )
                }
            )

            for bm in bound_methods:
                with Path(root, f"{bm}.rst").open("w") as f2:
                    title = f"{bm}()"

                    f2.write(title + "\n" + "=" * len(title) + "\n\n")
                    f2.write(f".. automethod:: pyrogram.types.{bm}()")

        f.write(template.format(**fmt_keys))


def start() -> None:
    global page_template, toctree  # noqa: PLW0603

    shutil.rmtree(DESTINATION, ignore_errors=True)

    with Path(HOME, "template/page.txt").open(encoding="utf-8") as f:
        page_template = f.read()

    with Path(HOME, "template/toctree.txt").open(encoding="utf-8") as f:
        toctree = f.read()

    generate(TYPES_PATH, TYPES_BASE)
    generate(FUNCTIONS_PATH, FUNCTIONS_BASE)
    generate(BASE_PATH, BASE_BASE)
    pyrogram_api()


if __name__ == "__main__":
    FUNCTIONS_PATH = "../../pyrogram/raw/functions"
    TYPES_PATH = "../../pyrogram/raw/types"
    BASE_PATH = "../../pyrogram/raw/base"
    HOME = "."
    DESTINATION = "../../docs/source/telegram"
    PYROGRAM_API_DEST = "../../docs/source/api"

    start()
