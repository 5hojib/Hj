from __future__ import annotations

import pyrogram
from pyrogram import errors, raw, types


class PromoteChatMember:
    async def promote_chat_member(
        self: pyrogram.Client,
        chat_id: int | str,
        user_id: int | str,
        privileges: types.ChatPrivileges = None,
        title: str | None = None,
    ) -> bool:
        """Promote or demote a user in a supergroup or a channel.

        You must be an administrator in the chat for this to work and must have the appropriate admin rights.
        Pass False for all boolean parameters to demote a user.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                You can also use chat public link in form of *t.me/<username>* (str).

            user_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target user.
                For a contact that exists in your Telegram address book you can use his phone number (str).
                You can also use user profile link in form of *t.me/<username>* (str).

            privileges (:obj:`~pyrogram.types.ChatPrivileges`, *optional*):
                New user privileges.

            title: (``str``, *optional*):
                A custom title that will be shown to all members instead of "Owner" or "Admin".
                Pass None or "" (empty string) will keep the current title.
                If you want to delete the custom title, use :meth:`~pyrogram.Client.set_administrator_title()` method.

        Returns:
            ``bool``: True on success.

        Example:
            .. code-block:: python

                # Promote chat member to admin
                await app.promote_chat_member(chat_id, user_id)
        """
        chat_id = await self.resolve_peer(chat_id)
        user_id = await self.resolve_peer(user_id)

        # See Chat.promote_member for the reason of this (instead of setting types.ChatPrivileges() as default arg).
        if privileges is None:
            privileges = types.ChatPrivileges()

        try:
            raw_chat_member = (
                await self.invoke(
                    raw.functions.channels.GetParticipant(
                        channel=chat_id,
                        participant=user_id,
                    ),
                )
            ).participant
        except errors.RPCError:
            raw_chat_member = None

        if not title and isinstance(
            raw_chat_member,
            raw.types.ChannelParticipantAdmin,
        ):
            rank = raw_chat_member.rank
        else:
            rank = title

        await self.invoke(
            raw.functions.channels.EditAdmin(
                channel=chat_id,
                user_id=user_id,
                admin_rights=raw.types.ChatAdminRights(
                    anonymous=privileges.is_anonymous,
                    change_info=privileges.can_change_info,
                    post_messages=privileges.can_post_messages,
                    edit_messages=privileges.can_edit_messages,
                    delete_messages=privileges.can_delete_messages,
                    ban_users=privileges.can_restrict_members,
                    invite_users=privileges.can_invite_users,
                    pin_messages=privileges.can_pin_messages,
                    add_admins=privileges.can_promote_members,
                    manage_call=privileges.can_manage_video_chats,
                    manage_topics=privileges.can_manage_topics,
                    post_stories=privileges.can_post_stories,
                    edit_stories=privileges.can_edit_stories,
                    delete_stories=privileges.can_delete_stories,
                    other=privileges.can_manage_chat,
                ),
                rank=rank or "",
            ),
        )

        return True
