# ruff: noqa: ARG002
from __future__ import annotations

import logging

from .tcp import TCP, Proxy

log = logging.getLogger(__name__)


class TCPAbridged(TCP):
    def __init__(self, ipv6: bool, proxy: Proxy) -> None:
        super().__init__(ipv6, proxy)

    async def connect(self, address: tuple[str, int]) -> None:
        await super().connect(address)
        await super().send(b"\xef")

    async def send(self, data: bytes, *args) -> None:
        length = len(data) // 4

        await super().send(
            (
                bytes([length])
                if length <= 126
                else b"\x7f" + length.to_bytes(3, "little")
            )
            + data,
        )

    async def recv(self, length: int = 0) -> bytes | None:
        length = await super().recv(1)

        if length is None:
            return None

        if length == b"\x7f":
            length = await super().recv(3)

            if length is None:
                return None

        return await super().recv(int.from_bytes(length, "little") * 4)
