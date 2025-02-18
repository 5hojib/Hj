from __future__ import annotations

import contextlib
import inspect
import time
from typing import TYPE_CHECKING, Any, NoReturn

from pyrogram import raw, utils

from .storage import Storage

if TYPE_CHECKING:
    import aiosqlite

# language=SQLite
SCHEMA = """
CREATE TABLE sessions
(
    dc_id     INTEGER PRIMARY KEY,
    api_id    INTEGER,
    test_mode INTEGER,
    auth_key  BLOB,
    date      INTEGER NOT NULL,
    user_id   INTEGER,
    is_bot    INTEGER
);

CREATE TABLE peers
(
    id             INTEGER PRIMARY KEY,
    access_hash    INTEGER,
    type           INTEGER NOT NULL,
    username       TEXT,
    phone_number   TEXT,
    last_update_on INTEGER NOT NULL DEFAULT (CAST(STRFTIME('%s', 'now') AS INTEGER))
);

CREATE TABLE update_state
(
    id   INTEGER PRIMARY KEY,
    pts  INTEGER,
    qts  INTEGER,
    date INTEGER,
    seq  INTEGER
);

CREATE TABLE version
(
    number INTEGER PRIMARY KEY
);

CREATE INDEX idx_peers_id ON peers (id);
CREATE INDEX idx_peers_username ON peers (username);
CREATE INDEX idx_peers_phone_number ON peers (phone_number);

CREATE TRIGGER trg_peers_last_update_on
    AFTER UPDATE
    ON peers
BEGIN
    UPDATE peers
    SET last_update_on = CAST(STRFTIME('%s', 'now') AS INTEGER)
    WHERE id = NEW.id;
END;
"""


UNAME_SCHEMA = """
CREATE TABLE IF NOT EXISTS usernames
(
    id             TEXT PRIMARY KEY,
    peer_id        INTEGER NOT NULL,
    last_update_on INTEGER NOT NULL DEFAULT (CAST(STRFTIME('%s', 'now') AS INTEGER))
);

CREATE TRIGGER IF NOT EXISTS trg_usernames_last_update_on
    AFTER UPDATE
    ON usernames
BEGIN
    UPDATE usernames
    SET last_update_on = CAST(STRFTIME('%s', 'now') AS INTEGER)
    WHERE id = NEW.id;
END;
"""


def get_input_peer(peer_id: int, access_hash: int, peer_type: str):
    if peer_type in ["user", "bot"]:
        return raw.types.InputPeerUser(user_id=peer_id, access_hash=access_hash)

    if peer_type == "group":
        return raw.types.InputPeerChat(chat_id=-peer_id)

    if peer_type in ["channel", "supergroup"]:
        return raw.types.InputPeerChannel(
            channel_id=utils.get_channel_id(peer_id),
            access_hash=access_hash,
        )

    raise ValueError(f"Invalid peer type: {peer_type}")


class SQLiteStorage(Storage):
    VERSION = 4
    USERNAME_TTL = 8 * 60 * 60

    def __init__(self, name: str) -> None:
        super().__init__(name)

        self.conn: aiosqlite.Connection = None

    async def create(self) -> None:
        await self.conn.executescript(SCHEMA)
        await self.conn.execute("INSERT INTO version VALUES (?)", (self.VERSION,))
        await self.conn.execute(
            "INSERT INTO sessions VALUES (?, ?, ?, ?, ?, ?, ?)",
            (2, None, None, None, 0, None, None),
        )
        await self.conn.commit()

    async def open(self) -> NoReturn:
        raise NotImplementedError

    async def save(self) -> None:
        await self.date(int(time.time()))
        await self.conn.commit()

    async def close(self) -> None:
        await self.conn.close()

    async def delete(self) -> NoReturn:
        raise NotImplementedError

    async def update_peers(
        self,
        peers: list[tuple[int, int, str, str, str]],
    ) -> None:
        with contextlib.suppress(Exception):
            await self.conn.executemany(
                "REPLACE INTO peers (id, access_hash, type, username, phone_number)"
                "VALUES (?, ?, ?, ?, ?)",
                peers,
            )

    async def update_usernames(self, usernames: list[tuple[int, str]]) -> None:
        await self.conn.executescript(UNAME_SCHEMA)
        for user in usernames:
            await self.conn.execute(
                "DELETE FROM usernames WHERE peer_id=?",
                (user[0],),
            )
        await self.conn.executemany(
            "REPLACE INTO usernames (peer_id, id)VALUES (?, ?)",
            usernames,
        )

    async def update_state(self, value: tuple[int, int, int, int, int] = object):
        if value is object:
            return await (
                await self.conn.execute(
                    "SELECT id, pts, qts, date, seq FROM update_state "
                    "ORDER BY date ASC",
                )
            ).fetchall()
        if isinstance(value, int):
            await self.conn.execute(
                "DELETE FROM update_state WHERE id = ?",
                (value,),
            )
        else:
            await self.conn.execute(
                "REPLACE INTO update_state (id, pts, qts, date, seq)"
                "VALUES (?, ?, ?, ?, ?)",
                value,
            )
        await self.conn.commit()
        return None

    async def get_peer_by_id(self, peer_id: int):
        q = await self.conn.execute(
            "SELECT id, access_hash, type FROM peers WHERE id = ?",
            (peer_id,),
        )
        r = await q.fetchone()

        if r is None:
            raise KeyError(f"ID not found: {peer_id}")

        return get_input_peer(*r)

    async def get_peer_by_username(self, username: str):
        q = await self.conn.execute(
            "SELECT id, access_hash, type, last_update_on FROM peers WHERE username = ?"
            "ORDER BY last_update_on DESC",
            (username,),
        )
        r = await q.fetchone()

        if r is None:
            r2 = await self.conn.execute(
                "SELECT peer_id, last_update_on FROM usernames WHERE id = ?"
                "ORDER BY last_update_on DESC",
                (username,),
            )
            r2 = await r2.fetchone()
            if r2 is None:
                raise KeyError(f"Username not found: {username}")
            if abs(time.time() - r2[1]) > self.USERNAME_TTL:
                raise KeyError(f"Username expired: {username}")
            r = await self.conn.execute(
                "SELECT id, access_hash, type, last_update_on FROM peers WHERE id = ?"
                "ORDER BY last_update_on DESC",
                (r2[0],),
            )
            r = await r.fetchone()
            if r is None:
                raise KeyError(f"Username not found: {username}")

        if abs(time.time() - r[3]) > self.USERNAME_TTL:
            raise KeyError(f"Username expired: {username}")

        return get_input_peer(*r[:3])

    async def get_peer_by_phone_number(self, phone_number: str):
        q = await self.conn.execute(
            "SELECT id, access_hash, type FROM peers WHERE phone_number = ?",
            (phone_number,),
        )
        r = await q.fetchone()

        if r is None:
            raise KeyError(f"Phone number not found: {phone_number}")

        return get_input_peer(*r)

    async def _get(self):
        attr = inspect.stack()[2].function

        q = await self.conn.execute(f"SELECT {attr} FROM sessions")
        row = await q.fetchone()
        return row[0] if row else None

    async def _set(self, value: Any) -> None:
        attr = inspect.stack()[2].function
        await self.conn.execute(f"UPDATE sessions SET {attr} = ?", (value,))
        await self.conn.commit()

    async def _accessor(self, value: Any = object):
        return await self._get() if value is object else await self._set(value)

    async def dc_id(self, value: int = object):
        return await self._accessor(value)

    async def api_id(self, value: int = object):
        return await self._accessor(value)

    async def test_mode(self, value: bool = object):
        return await self._accessor(value)

    async def auth_key(self, value: bytes = object):
        return await self._accessor(value)

    async def date(self, value: int = object):
        return await self._accessor(value)

    async def user_id(self, value: int = object):
        return await self._accessor(value)

    async def is_bot(self, value: bool = object):
        return await self._accessor(value)

    async def version(self, value: int = object):
        if value is object:
            q = await self.conn.execute("SELECT number FROM version")
            row = await q.fetchone()
            return row[0] if row else None
        await self.conn.execute("UPDATE version SET number = ?", (value,))
        await self.conn.commit()
        return None
