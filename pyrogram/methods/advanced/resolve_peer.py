from __future__ import annotations

import logging
import re

import pyrogram
from pyrogram import raw, utils
from pyrogram.errors import PeerIdInvalid

log = logging.getLogger(__name__)


class ResolvePeer:
    async def resolve_peer(
        self: pyrogram.Client,
        peer_id: int | str,
    ) -> raw.base.InputPeer | raw.base.InputUser | raw.base.InputChannel:
        """Get the InputPeer of a known peer id.
        Useful whenever an InputPeer type is required.

        .. note::

            This is a utility method intended to be used **only** when working with raw
            :obj:`functions <pyrogram.api.functions>` (i.e: a Telegram API method you wish to use which is not
            available yet in the Client class as an easy-to-use method).

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            peer_id (``int`` | ``str``):
                The peer id you want to extract the InputPeer from.
                Can be a direct id (int), a username (str) or a phone number (str) or *t.me/<username>* link.

        Returns:
            ``InputPeer``: On success, the resolved peer id is returned in form of an InputPeer object.

        Raises:
            KeyError: In case the peer doesn't exist in the internal database.
        """
        if not self.is_connected:
            raise ConnectionError("Client has not been started yet")

        if peer_id in ("self", "me"):
            return raw.types.InputPeerSelf()
        try:
            return await self.storage.get_peer_by_id(peer_id)
        except KeyError:
            if isinstance(peer_id, str):
                peer_id = re.sub(r"[@+\s]", "", peer_id.lower())
                peer_id = re.sub(r"https://t.me/", "", peer_id.lower())

                try:
                    int(peer_id)
                except ValueError:
                    try:
                        return await self.storage.get_peer_by_username(peer_id)
                    except KeyError:
                        await self.invoke(
                            raw.functions.contacts.ResolveUsername(username=peer_id),
                        )

                        return await self.storage.get_peer_by_username(peer_id)
                else:
                    try:
                        return await self.storage.get_peer_by_phone_number(peer_id)
                    except KeyError:
                        raise PeerIdInvalid from None

            peer_type = utils.get_peer_type(peer_id)

            if peer_type == "user":
                await self.fetch_peers(
                    await self.invoke(
                        raw.functions.users.GetUsers(
                            id=[raw.types.InputUser(user_id=peer_id, access_hash=0)],
                        ),
                    ),
                )
            elif peer_type == "chat":
                await self.invoke(raw.functions.messages.GetChats(id=[-peer_id]))
            else:
                await self.invoke(
                    raw.functions.channels.GetChannels(
                        id=[
                            raw.types.InputChannel(
                                channel_id=utils.get_channel_id(peer_id),
                                access_hash=0,
                            ),
                        ],
                    ),
                )

            try:
                return await self.storage.get_peer_by_id(peer_id)
            except KeyError:
                raise PeerIdInvalid from None
