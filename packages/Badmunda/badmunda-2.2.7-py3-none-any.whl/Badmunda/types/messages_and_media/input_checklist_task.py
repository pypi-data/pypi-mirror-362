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

from typing import List, Optional

import Badmunda
from Badmunda import enums, raw, types, utils

from ..object import Object


class InputChecklistTask(Object):
    """Describes a task in a checklist to be sent.

    Parameters:
        id (``int``):
            Unique identifier of the task.

        text (``str``):
            Text of the task.

        parse_mode (:obj:`~Badmunda.enums.ParseMode`, *optional*):
            The parse mode to use for the checklist.

        entities (List of :obj:`~Badmunda.types.MessageEntity`, *optional*):
            List of special entities that appear in the checklist title.
    """

    def __init__(
        self,
        *,
        id: int,
        text: str,
        parse_mode: Optional["enums.ParseMode"] = None,
        entities: Optional[List["types.MessageEntity"]] = None,
    ):
        super().__init__()

        self.id = id
        self.text = text
        self.parse_mode = parse_mode
        self.entities = entities

    async def write(
        self, client: "Badmunda.Client"
    ) -> "raw.types.TodoItem":
        task_title, task_entities = (await utils.parse_text_entities(
            client, self.text, self.parse_mode, self.entities
        )).values()

        return raw.types.TodoItem(
            id=self.id,
            title=raw.types.TextWithEntities(
                text=task_title,
                entities=task_entities or []
            )
        )
