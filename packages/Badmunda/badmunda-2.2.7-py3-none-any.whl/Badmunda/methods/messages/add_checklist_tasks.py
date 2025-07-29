#  Badmunda - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Badmunda.
#
#  Badmunda is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Badmunda is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Badmunda.  If not, see <http://www.gnu.org/licenses/>.

from typing import List, Union

import Badmunda
from Badmunda import raw, types


class AddChecklistTasks:
    async def add_checklist_tasks(
        self: "Badmunda.Client",
        chat_id: Union[int, str],
        message_id: int,
        tasks: List["types.InputChecklistTask"]
    ) -> int:
        """Add tasks to a checklist in a message.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            message_id (``int``):
                Identifier of the message containing the checklist.

            tasks (List of :obj:`~Badmunda.types.InputChecklistTask`):
                List of tasks to add to the checklist.

        Returns:
            ``bool``: On success, True is returned.

        Example:
            .. code-block:: python

                await app.add_checklist_tasks(
                    chat_id,
                    message_id,
                    tasks=[
                        types.InputChecklistTask(
                            id=2,
                            text="Task 2"
                        )
                    ]
                )
        """
        await self.invoke(
            raw.functions.messages.AppendTodoList(
                peer=await self.resolve_peer(chat_id),
                msg_id=message_id,
                list=[await task.write(self) for task in tasks]
            )
        )

        return True
