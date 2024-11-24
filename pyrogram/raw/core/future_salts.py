from __future__ import annotations

from io import BytesIO
from typing import Any

from .future_salt import FutureSalt
from .primitives.int import Int, Long
from .tl_object import TLObject


class FutureSalts(TLObject):
    ID = 0xAE500895

    __slots__ = ["now", "req_msg_id", "salts"]

    QUALNAME = "FutureSalts"

    def __init__(self, req_msg_id: int, now: int, salts: list[FutureSalt]) -> None:
        self.req_msg_id = req_msg_id
        self.now = now
        self.salts = salts

    @staticmethod
    def read(data: BytesIO, *args: Any) -> FutureSalts:  # noqa: ARG004
        req_msg_id = Long.read(data)
        now = Int.read(data)

        count = Int.read(data)
        salts = [FutureSalt.read(data) for _ in range(count)]

        return FutureSalts(req_msg_id, now, salts)

    def write(self, *args: Any) -> bytes:  # noqa: ARG002
        b = BytesIO()

        b.write(Int(self.ID, False))

        b.write(Long(self.req_msg_id))
        b.write(Int(self.now))

        count = len(self.salts)
        b.write(Int(count))

        for salt in self.salts:
            b.write(salt.write())

        return b.getvalue()
