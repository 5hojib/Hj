#  Pyrofork - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#  Copyright (C) 2022-present Mayuri-Chan <https://github.com/Mayuri-Chan>
#
#  This file is part of Pyrofork.
#
#  Pyrofork is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrofork is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrofork.  If not, see <http://www.gnu.org/licenses/>.

from io import BytesIO
from typing import Any

from pyrogram.raw.core.tl_object import TLObject


class Int(bytes, TLObject):
    SIZE = 4

    @classmethod
    def read(
        cls, data: BytesIO, signed: bool = True, *args: Any
    ) -> int:
        return int.from_bytes(
            data.read(cls.SIZE), "little", signed=signed
        )

    def __new__(cls, value: int, signed: bool = True) -> bytes:  # type: ignore
        return value.to_bytes(cls.SIZE, "little", signed=signed)


class Long(Int):
    SIZE = 8


class Int128(Int):
    SIZE = 16


class Int256(Int):
    SIZE = 32
