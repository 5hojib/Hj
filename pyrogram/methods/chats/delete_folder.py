from __future__ import annotations

import pyrogram
from pyrogram import raw


class DeleteFolder:
    async def delete_folder(self: pyrogram.Client, folder_id: int) -> bool:
        """Delete a user's folder.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            folder_id (``int``):
                Unique identifier (int) of the target folder.

        Returns:
            ``bool``: True, on success.

        Example:
            .. code-block:: python

                # Delete folder
                app.delete_folder(folder_id)
        """
        return await self.invoke(
            raw.functions.messages.UpdateDialogFilter(id=folder_id),
        )
