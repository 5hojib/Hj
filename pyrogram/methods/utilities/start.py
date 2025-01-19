from __future__ import annotations

import logging

import pyrogram
from pyrogram import raw

log = logging.getLogger(__name__)


class Start:
    async def start(self: pyrogram.Client):
        """Start the client.

        This method connects the client to Telegram and, in case of new sessions, automatically manages the
        authorization process using an interactive prompt.

        Returns:
            :obj:`~pyrogram.Client`: The started client itself.

        Raises:
            ConnectionError: In case you try to start an already started client.

        Example:
            .. code-block:: python

                from pyrogram import Client

                app = Client("my_account")


                async def main():
                    await app.start()
                    ...  # Invoke API methods
                    await app.stop()


                app.run(main())
        """
        is_authorized = await self.connect()

        try:
            if not is_authorized:
                await self.authorize()

            if self.takeout and not await self.storage.is_bot():
                self.takeout_id = (
                    await self.invoke(raw.functions.account.InitTakeoutSession())
                ).id
                log.info("Takeout session %s initiated", self.takeout_id)

            await self.invoke(raw.functions.updates.GetState())
        except (Exception, KeyboardInterrupt):
            await self.disconnect()
            raise
        else:
            self.me = await self.get_me()
            await self.initialize()

            return self
