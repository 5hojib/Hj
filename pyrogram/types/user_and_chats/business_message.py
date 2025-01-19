from __future__ import annotations

from typing import TYPE_CHECKING

from pyrogram import enums, raw, types, utils
from pyrogram.types.object import Object

if TYPE_CHECKING:
    from datetime import datetime


class BusinessMessage(Object):
    """Business working hours.

    Parameters:
        shortcut_id (``int``):
            ID of the shortcut.

        is_greeting (``bool``, *optional*):
            True, if the message is a greeting message.

        is_away (``bool``, *optional*):
            True, if the message is an away message.

        no_activity_days (``int``, *optional*):
            Period of inactivity after which the greeting message should be sent again.

        offline_only (``bool``, *optional*):
            Dont send the away message if you've recently been online.

        recipients (List of :obj:`~pyrogram.types.User`, *optional*):
            Recipients of the message.

        schedule (:obj:`~pyrogram.enums.BusinessSchedule`, *optional*):
            Schedule of the away message to be sent.

        start_date (``datetime``, *optional*):
            Start date of the away message.

        end_date (``datetime``, *optional*):
            End date of the away message.
    """

    def __init__(
        self,
        *,
        shortcut_id: int,
        is_greeting: bool | None = None,
        is_away: bool | None = None,
        no_activity_days: int | None = None,
        offline_only: bool | None = None,
        recipients: list[types.User] | None = None,
        schedule: enums.BusinessSchedule = None,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
    ) -> None:
        self.shortcut_id = shortcut_id
        self.is_greeting = is_greeting
        self.is_away = is_away
        self.no_activity_days = no_activity_days
        self.offline_only = offline_only
        self.recipients = recipients
        self.schedule = schedule
        self.start_date = start_date
        self.end_date = end_date

    @staticmethod
    def _parse(
        client,
        message: raw.types.BusinessGreetingMessage
        | raw.types.BusinessAwayMessage = None,
        users: dict | None = None,
    ) -> BusinessMessage | None:
        if not message:
            return None

        schedule = None

        if isinstance(message, raw.types.BusinessAwayMessage):
            if isinstance(
                message.schedule,
                raw.types.BusinessAwayMessageScheduleAlways,
            ):
                schedule = enums.BusinessSchedule.ALWAYS
            elif isinstance(
                message.schedule,
                raw.types.BusinessAwayMessageScheduleOutsideWorkHours,
            ):
                schedule = enums.BusinessSchedule.OUTSIDE_WORK_HOURS
            elif isinstance(
                message.schedule,
                raw.types.BusinessAwayMessageScheduleCustom,
            ):
                schedule = enums.BusinessSchedule.CUSTOM

        return BusinessMessage(
            shortcut_id=message.shortcut_id,
            is_greeting=isinstance(message, raw.types.BusinessGreetingMessage),
            is_away=isinstance(message, raw.types.BusinessAwayMessage),
            no_activity_days=getattr(message, "no_activity_days", None),
            offline_only=getattr(message, "offline_only", None),
            recipients=types.BusinessRecipients._parse(
                client,
                message.recipients,
                users,
            ),
            schedule=schedule,
            start_date=utils.timestamp_to_datetime(message.schedule.start_date)
            if schedule == enums.BusinessSchedule.CUSTOM
            else None,
            end_date=utils.timestamp_to_datetime(message.schedule.end_date)
            if schedule == enums.BusinessSchedule.CUSTOM
            else None,
        )
