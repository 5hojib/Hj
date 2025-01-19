from __future__ import annotations

from typing import TYPE_CHECKING

import pyrogram
from pyrogram.filters import Filter

if TYPE_CHECKING:
    from collections.abc import Callable


class OnChatJoinRequest:
    def on_chat_join_request(self=None, filters=None, group: int = 0) -> Callable:
        """Decorator for handling chat join requests.

        This does the same thing as :meth:`~pyrogram.Client.add_handler` using the
        :obj:`~pyrogram.handlers.ChatJoinRequestHandler`.

        Parameters:
            filters (:obj:`~pyrogram.filters`, *optional*):
                Pass one or more filters to allow only a subset of updates to be passed in your function.

            group (``int``, *optional*):
                The group identifier, defaults to 0.
        """

        def decorator(func: Callable) -> Callable:
            if isinstance(self, pyrogram.Client):
                self.add_handler(
                    pyrogram.handlers.ChatJoinRequestHandler(func, filters),
                    group,
                )
            elif isinstance(self, Filter) or self is None:
                if not hasattr(func, "handlers"):
                    func.handlers = []

                func.handlers.append(
                    (
                        pyrogram.handlers.ChatJoinRequestHandler(func, self),
                        group if filters is None else filters,
                    ),
                )

            return func

        return decorator
