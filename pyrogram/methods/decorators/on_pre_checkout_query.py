from __future__ import annotations

from typing import TYPE_CHECKING

import pyrogram
from pyrogram.filters import Filter

if TYPE_CHECKING:
    from collections.abc import Callable


class OnPreCheckoutQuery:
    def on_pre_checkout_query(
        self: OnPreCheckoutQuery | Filter | None = None,
        filters: Filter | None = None,
        group: int = 0,
    ) -> Callable:
        """Decorator for handling pre-checkout queries.

        This does the same thing as :meth:`~pyrogram.Client.add_handler` using the
        :obj:`~pyrogram.handlers.PreCheckoutQueryHandler`.

        Parameters:
            filters (:obj:`~pyrogram.filters`, *optional*):
                Pass one or more filters to allow only a subset of callback queries to be passed
                in your function.

            group (``int``, *optional*):
                The group identifier, defaults to 0.
        """

        def decorator(func: Callable) -> Callable:
            if isinstance(self, pyrogram.Client):
                self.add_handler(
                    pyrogram.handlers.PreCheckoutQueryHandler(func, filters),
                    group,
                )
            elif isinstance(self, Filter) or self is None:
                if not hasattr(func, "handlers"):
                    func.handlers = []

                func.handlers.append(
                    (
                        pyrogram.handlers.PreCheckoutQueryHandler(func, self),
                        group if filters is None else filters,
                    ),
                )

            return func

        return decorator
