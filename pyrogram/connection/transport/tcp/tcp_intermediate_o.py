# ruff: noqa: ARG002
from __future__ import annotations

import logging
import os
from struct import pack, unpack

from pyrogram.crypto import aes

from .tcp import TCP, Proxy

log = logging.getLogger(__name__)


class TCPIntermediateO(TCP):
    RESERVED = (b"HEAD", b"POST", b"GET ", b"OPTI", b"\xee" * 4)

    def __init__(self, ipv6: bool, proxy: Proxy) -> None:
        super().__init__(ipv6, proxy)

        self.encrypt = None
        self.decrypt = None

    async def connect(self, address: tuple[str, int]) -> None:
        await super().connect(address)

        while True:
            nonce = bytearray(os.urandom(64))

            if (
                bytes([nonce[0]]) != b"\xef"
                and nonce[:4] not in self.RESERVED
                and nonce[4:8] != b"\x00" * 4
            ):
                nonce[56] = nonce[57] = nonce[58] = nonce[59] = 0xEE
                break

        temp = bytearray(nonce[55:7:-1])

        self.encrypt = (nonce[8:40], nonce[40:56], bytearray(1))
        self.decrypt = (temp[0:32], temp[32:48], bytearray(1))

        nonce[56:64] = aes.ctr256_encrypt(nonce, *self.encrypt)[56:64]

        await super().send(nonce)

    async def send(self, data: bytes, *args) -> None:
        await super().send(
            aes.ctr256_encrypt(pack("<i", len(data)) + data, *self.encrypt),
        )

    async def recv(self, length: int = 0) -> bytes | None:
        length = await super().recv(4)

        if length is None:
            return None

        length = aes.ctr256_decrypt(length, *self.decrypt)

        data = await super().recv(unpack("<i", length)[0])

        if data is None:
            return None

        return aes.ctr256_decrypt(data, *self.decrypt)
