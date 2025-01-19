from __future__ import annotations

from typing import TYPE_CHECKING, Any, cast

from pyrogram.raw.core.list import List
from pyrogram.raw.core.tl_object import TLObject

from .bool import Bool, BoolFalse, BoolTrue
from .int import Int, Long

if TYPE_CHECKING:
    from io import BytesIO


class Vector(bytes, TLObject):
    ID = 0x1CB5C415

    @staticmethod
    def read_bare(b: BytesIO, size: int) -> int | Any:
        if size == 4:
            e = int.from_bytes(b.read(4), "little")
            b.seek(-4, 1)

            if e in {BoolFalse.ID, BoolTrue.ID}:
                return Bool.read(b)

            return Int.read(b)

        if size == 8:
            return Long.read(b)

        return TLObject.read(b)

    @classmethod
    def read(cls, data: BytesIO, t: Any = None, *args: Any) -> List:  # noqa: ARG003
        count = Int.read(data)
        left = len(data.read())
        size = (left / count) if count else 0
        data.seek(-left, 1)

        return List(
            t.read(data) if t else Vector.read_bare(data, size) for _ in range(count)
        )

    def __new__(cls, value: list, t: Any = None) -> bytes:  # type: ignore
        return b"".join(
            [Int(cls.ID, False), Int(len(value))]
            + [cast(bytes, t(i)) if t else i.write() for i in value],
        )
