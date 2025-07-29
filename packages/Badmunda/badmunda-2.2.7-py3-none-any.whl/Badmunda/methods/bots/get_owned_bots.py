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


class GetOwnedBots:
    async def get_owned_bots(
        self: "Badmunda.Client",
    ) -> List["types.User"]:
        """Returns the list of bots owned by the current user.

        .. include:: /_includes/usable-by/users.rst

        Returns:
            List of :obj:`~Badmunda.types.User`: On success.

        Example:
            .. code-block:: python

                bots = await app.get_owned_bots()
        """

        bots = await self.invoke(raw.functions.bots.GetAdminedBots())

        return types.List([types.User._parse(self, bot) for bot in bots])
