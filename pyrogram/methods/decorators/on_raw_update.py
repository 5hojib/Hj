from __future__ import annotations

from typing import TYPE_CHECKING

import pyrogram

if TYPE_CHECKING:
    from collections.abc import Callable


class OnRawUpdate:
    def on_raw_update(self=None, group: int = 0) -> Callable:
        """Decorator for handling raw updates.

        This does the same thing as :meth:`~pyrogram.Client.add_handler` using the
        :obj:`~pyrogram.handlers.RawUpdateHandler`.

        Parameters:
            group (``int``, *optional*):
                The group identifier, defaults to 0.
        """

        def decorator(func: Callable) -> Callable:
            if isinstance(self, pyrogram.Client):
                self.add_handler(pyrogram.handlers.RawUpdateHandler(func), group)
            else:
                if not hasattr(func, "handlers"):
                    func.handlers = []

                func.handlers.append(
                    (pyrogram.handlers.RawUpdateHandler(func), group),
                )

            return func

        return decorator
