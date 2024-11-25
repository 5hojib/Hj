from __future__ import annotations

from typing import TYPE_CHECKING, Any, TypeVar

from pyrogram import utils

if TYPE_CHECKING:
    from collections.abc import Callable


class RunSync:
    Result = TypeVar("Result")

    async def run_sync(
        self,
        func: Callable[..., Result],
        *args: Any,
        **kwargs: Any,
    ) -> Result:
        """Runs the given sync function (optionally with arguments) on a separate thread.

        Parameters:
            func (``Callable``):
                Sync function to run.

            \\*args (``any``, *optional*):
                Function argument.

            \\*\\*kwargs (``any``, *optional*):
                Function extras arguments.

        Returns:
                ``any``: The function result.
        """

        return await utils.run_sync(func, *args, **kwargs)
