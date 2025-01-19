from __future__ import annotations

import base64
import logging
import struct

import aiosqlite

from .sqlite_storage import SQLiteStorage

log = logging.getLogger(__name__)


class MemoryStorage(SQLiteStorage):
    def __init__(
        self,
        name: str,
        session_string: str | None = None,
        is_telethon_string: bool = False,
    ) -> None:
        super().__init__(name)

        self.session_string = session_string
        self.is_telethon_string = is_telethon_string

    async def open(self) -> None:
        self.conn = await aiosqlite.connect(":memory:")
        await self.create()

        if self.session_string:
            # Old format
            if len(self.session_string) in [
                self.SESSION_STRING_SIZE,
                self.SESSION_STRING_SIZE_64,
            ]:
                dc_id, test_mode, auth_key, user_id, is_bot = struct.unpack(
                    (
                        self.OLD_SESSION_STRING_FORMAT
                        if len(self.session_string) == self.SESSION_STRING_SIZE
                        else self.OLD_SESSION_STRING_FORMAT_64
                    ),
                    base64.urlsafe_b64decode(
                        self.session_string + "=" * (-len(self.session_string) % 4),
                    ),
                )

                await self.dc_id(dc_id)
                await self.test_mode(test_mode)
                await self.auth_key(auth_key)
                await self.user_id(user_id)
                await self.is_bot(is_bot)
                await self.date(0)

                log.warning(
                    "You are using an old session string format. Use export_session_string to update",
                )
                return
            if self.is_telethon_string:
                # Telethon format
                string = self.session_string[1:]
                ip_len = 4 if len(string) == 352 else 16
                dc_id, ip, port, auth_key = struct.unpack(
                    f">B{ip_len}sH256s",
                    base64.urlsafe_b64decode(string),
                )
                api_id = 0
                test_mode = False
                user_id = 9999
                is_bot = False
            else:
                dc_id, api_id, test_mode, auth_key, user_id, is_bot = struct.unpack(
                    self.SESSION_STRING_FORMAT,
                    base64.urlsafe_b64decode(
                        self.session_string + "=" * (-len(self.session_string) % 4),
                    ),
                )

            await self.dc_id(dc_id)
            await self.api_id(api_id)
            await self.test_mode(test_mode)
            await self.auth_key(auth_key)
            await self.user_id(user_id)
            await self.is_bot(is_bot)
            await self.date(0)

    async def delete(self) -> None:
        pass
