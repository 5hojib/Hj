from __future__ import annotations

import logging
import sqlite3
from pathlib import Path

from .sqlite_storage import SQLiteStorage

log = logging.getLogger(__name__)

USERNAMES_SCHEMA = """
CREATE TABLE usernames
(
    id       INTEGER,
    username TEXT,
    FOREIGN KEY (id) REFERENCES peers(id)
);

CREATE INDEX idx_usernames_username ON usernames (username);
"""

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

    def _vacuum(self):
        with self.conn:
            self.conn.execute("VACUUM")

    def _update_from_one_impl(self):
        with self.conn:
            self.conn.execute("DELETE FROM peers")

    def _update_from_two_impl(self):
        with self.conn:
            self.conn.execute("ALTER TABLE sessions ADD api_id INTEGER")

    def _update_from_three_impl(self):
        with self.conn:
            self.conn.executescript(USERNAMES_SCHEMA)

    def _update_from_four_impl(self):
        with self.conn:
            self.conn.executescript(UPDATE_STATE_SCHEMA)

    def _update_from_five_impl(self):
        with self.conn:
            self.conn.executescript(
                "CREATE INDEX idx_usernames_id ON usernames (id);"
            )

    def _connect_impl(self, path):
        self.conn = sqlite3.connect(str(path), timeout=1, check_same_thread=False)

        with self.conn:
            self.conn.execute("PRAGMA journal_mode=WAL").close()
            self.conn.execute("PRAGMA synchronous=NORMAL").close()
            self.conn.execute("PRAGMA temp_store=1").close()

    async def update(self):
        version = await self.version()

        if version == 1:
            await self.loop.run_in_executor(
                self.executor, self._update_from_one_impl
            )
            version += 1

        if version == 2:
            await self.loop.run_in_executor(
                self.executor, self._update_from_two_impl
            )
            version += 1

        if version == 3:
            await self.loop.run_in_executor(
                self.executor, self._update_from_three_impl
            )
            version += 1

        if version == 4:
            await self.loop.run_in_executor(
                self.executor, self._update_from_four_impl
            )
            version += 1

        if version == 5:
            await self.loop.run_in_executor(
                self.executor, self._update_from_five_impl
            )
            version += 1

        await self.version(version)

    async def open(self) -> None:
        path = self.database
        file_exists = path.is_file()

        self.executor.submit(self._connect_impl, path).result()

        if not file_exists:
            await self.create()
        else:
            await self.update()

        await self.loop.run_in_executor(self.executor, self._vacuum)

    async def delete(self) -> None:
        Path(self.database).unlink()
