from __future__ import annotations

from typing import TYPE_CHECKING

from pyrogram.handlers import DisconnectHandler

if TYPE_CHECKING:
    import pyrogram
    from pyrogram.handlers.handler import Handler


class RemoveHandler:
    def remove_handler(
        self: pyrogram.Client,
        handler: Handler,
        group: int = 0,
    ) -> None:
        """Remove a previously-registered update handler.

        Make sure to provide the right group where the handler was added in. You can use the return value of the
        :meth:`~pyrogram.Client.add_handler` method, a tuple of *(handler, group)*, and pass it directly.

        Parameters:
            handler (``Handler``):
                The handler to be removed.

            group (``int``, *optional*):
                The group identifier, defaults to 0.

        Example:
            .. code-block:: python

                from pyrogram import Client
                from pyrogram.handlers import MessageHandler

                async def hello(client, message):
                    print(message)

                app = Client("my_account")

                handler = app.add_handler(MessageHandler(hello))

                # Starred expression to unpack (handler, group)
                app.remove_handler(*handler)

                app.run()
        """
        if isinstance(handler, DisconnectHandler):
            self.disconnect_handler = None
        else:
            self.dispatcher.remove_handler(handler, group)
