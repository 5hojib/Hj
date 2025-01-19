from __future__ import annotations

from typing import TYPE_CHECKING

import pyrogram
from pyrogram.filters import Filter

if TYPE_CHECKING:
    from collections.abc import Callable


class OnBotBusinessConnect:
    def on_bot_business_connect(self=None, filters=None, group: int = 0) -> Callable:
        """Decorator for handling bot business connection.

        This does the same thing as :meth:`~pyrogram.Client.add_handler` using the
        :obj:`~pyrogram.handlers.BotBusinessConnectHandler`.

        Parameters:
            filters (:obj:`~pyrogram.filters`, *optional*):
                Pass one or more filters to allow only a subset of stories to be passed
                in your function.

            group (``int``, *optional*):
                The group identifier, defaults to 0.
        """

        def decorator(func: Callable) -> Callable:
            if isinstance(self, pyrogram.Client):
                self.add_handler(
                    pyrogram.handlers.BotBusinessConnectHandler(func, filters),
                    group,
                )
            elif isinstance(self, Filter) or self is None:
                if not hasattr(func, "handlers"):
                    func.handlers = []

                func.handlers.append(
                    (
                        pyrogram.handlers.BotBusinessConnectHandler(func, self),
                        group if filters is None else filters,
                    ),
                )

            return func

        return decorator
