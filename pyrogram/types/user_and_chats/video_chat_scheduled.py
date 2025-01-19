from __future__ import annotations

from typing import TYPE_CHECKING

from pyrogram import raw, utils
from pyrogram.types.object import Object

if TYPE_CHECKING:
    from datetime import datetime


class VideoChatScheduled(Object):
    """A service message about a voice chat scheduled in the chat.

    Parameters:
        start_date (:py:obj:`~datetime.datetime`):
            Point in time when the voice chat is supposed to be started by a chat administrator.
    """

    def __init__(self, *, start_date: datetime) -> None:
        super().__init__()

        self.start_date = start_date

    @staticmethod
    def _parse(
        action: raw.types.MessageActionGroupCallScheduled,
    ) -> VideoChatScheduled:
        return VideoChatScheduled(
            start_date=utils.timestamp_to_datetime(action.schedule_date),
        )
