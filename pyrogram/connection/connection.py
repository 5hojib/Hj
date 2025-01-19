from __future__ import annotations

import asyncio
import logging

from pyrogram.session.internals import DataCenter

from .transport import TCP, TCPAbridged

log = logging.getLogger(__name__)


class Connection:
    MAX_CONNECTION_ATTEMPTS = 3

    def __init__(
        self,
        dc_id: int,
        test_mode: bool,
        ipv6: bool,
        alt_port: bool,
        proxy: dict,
        media: bool = False,
        protocol_factory: type[TCP] = TCPAbridged,
    ) -> None:
        self.dc_id = dc_id
        self.test_mode = test_mode
        self.ipv6 = ipv6
        self.alt_port = alt_port
        self.proxy = proxy
        self.media = media
        self.protocol_factory = protocol_factory

        self.address = DataCenter(dc_id, test_mode, ipv6, alt_port, media)
        self.protocol: TCP | None = None

    async def connect(self) -> None:
        for _i in range(Connection.MAX_CONNECTION_ATTEMPTS):
            self.protocol = self.protocol_factory(ipv6=self.ipv6, proxy=self.proxy)

            try:
                log.info("Connecting...")
                await self.protocol.connect(self.address)
            except OSError as e:
                log.warning("Unable to connect due to network issues: %s", e)
                await self.protocol.close()
                await asyncio.sleep(1)
            else:
                log.info(
                    "Connected! %s DC%s%s - IPv%s",
                    "Test" if self.test_mode else "Production",
                    self.dc_id,
                    " (media)" if self.media else "",
                    "6" if self.ipv6 else "4",
                )
                break
        else:
            log.warning("Connection failed! Trying again...")
            raise ConnectionError

    async def close(self) -> None:
        await self.protocol.close()
        log.info("Disconnected")

    async def send(self, data: bytes) -> None:
        await self.protocol.send(data)

    async def recv(self) -> bytes | None:
        return await self.protocol.recv()
