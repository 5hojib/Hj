from __future__ import annotations

import logging
from pathlib import Path

import aiosqlite

from .sqlite_storage import SQLiteStorage

log = logging.getLogger(__name__)

UPDATE_STATE_SCHEMA = """
CREATE TABLE update_state
(
    id   INTEGER PRIMARY KEY,
    pts  INTEGER,
    qts  INTEGER,
    date INTEGER,
    seq  INTEGER
);
"""


class FileStorage(SQLiteStorage):
    FILE_EXTENSION = ".session"

    def __init__(self, name: str, workdir: Path) -> None:
        super().__init__(name)

        self.database = workdir / (self.name + self.FILE_EXTENSION)

    async def update(self) -> None:
        version = await self.version()

        if version == 1:
            await self.conn.execute("DELETE FROM peers")
            await self.conn.commit()

            version += 1

        if version == 2:
            await self.conn.execute("ALTER TABLE sessions ADD api_id INTEGER")
            await self.conn.commit()

            version += 1

        if version == 3:
            await self.conn.execute(UPDATE_STATE_SCHEMA)
            await self.conn.commit()

            version += 1

        await self.version(version)

    async def open(self) -> None:
        path = self.database
        file_exists = path.is_file()

        self.conn = await aiosqlite.connect(str(path), timeout=1)

        await self.conn.execute("PRAGMA journal_mode=WAL")

        if not file_exists:
            await self.create()
        else:
            await self.update()

        await self.conn.execute("VACUUM")
        await self.conn.commit()

    async def delete(self) -> None:
        Path(self.database).unlink()
