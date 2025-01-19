from __future__ import annotations

from pyrogram import raw, types
from pyrogram.types.object import Object


class BusinessInfo(Object):
    """Business information of a user.

    Parameters:
        address (``str``, *optional*):
            Address of the business.

        location (:obj:`~pyrogram.types.Location`, *optional*):
            Location of the business on the map.

        greeting_message (:obj:`~pyrogram.types.BusinessMessage`, *optional*):
            Greeting message of the business.

        away_message (:obj:`~pyrogram.types.BusinessMessage`, *optional*):
            Away message of the business.

        working_hours (:obj:`~pyrogram.types.BusinessWorkingHours`, *optional*):
            Working hours of the business.
    """

    def __init__(
        self,
        *,
        address: str | None = None,
        location: types.Location = None,
        greeting_message: types.BusinessMessage = None,
        away_message: types.BusinessMessage = None,
        working_hours: types.BusinessWorkingHours = None,
    ) -> None:
        self.address = address
        self.location = location
        self.greeting_message = greeting_message
        self.away_message = away_message
        self.working_hours = working_hours

    @staticmethod
    def _parse(
        client,
        user: raw.types.UserFull = None,
        users: dict | None = None,
    ) -> BusinessInfo | None:
        working_hours = getattr(user, "business_work_hours", None)
        location = getattr(user, "business_location", None)
        greeting_message = getattr(user, "business_greeting_message", None)
        away_message = getattr(user, "business_away_message", None)

        if not any((working_hours, location, greeting_message, away_message)):
            return None

        return BusinessInfo(
            address=getattr(location, "address", None),
            location=types.Location._parse(
                client,
                getattr(location, "geo_point", None),
            ),
            greeting_message=types.BusinessMessage._parse(
                client,
                greeting_message,
                users,
            ),
            away_message=types.BusinessMessage._parse(client, away_message, users),
            working_hours=types.BusinessWorkingHours._parse(working_hours),
        )
