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

from typing import List

import Badmunda
from Badmunda import raw, types


class GetSuitableDiscussionChats:
    async def get_suitable_discussion_chats(
        self: "Badmunda.Client"
    ) -> List["types.Chat"]:
        """Return a list of basic group and supergroup chats, which can be used as a discussion group for a channel.

        Returned basic group chats must be first upgraded to supergroups before they can be set as a discussion group.

        .. include:: /_includes/usable-by/users.rst

        Returns:
            List of :obj:`~Badmunda.types.Chat`: List of suitable discussion chats.

        Example:
            .. code-block:: python

                chats = await app.get_suitable_discussion_chats()
        """
        r = await self.invoke(
            raw.functions.channels.GetGroupsForDiscussion()
        )

        return types.List([types.Chat._parse_chat(self, i) for i in r.chats])
