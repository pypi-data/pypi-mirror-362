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

import Badmunda
from Badmunda import raw


class SearchPostsCount:
    async def search_posts_count(
        self: "Badmunda.Client",
        hashtag: str,
    ) -> int:
        """Get the count of posts with hashtag resulting from a search.

        If you want to get the actual posts, see :meth:`~Badmunda.Client.search_posts`.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            hashtag (``str``):
                Text query string.

        Returns:
            ``int``: On success, the posts count is returned.
        """
        r = await self.invoke(
            raw.functions.channels.SearchPosts(
                hashtag=hashtag,
                offset_rate=0,
                offset_peer=raw.types.InputPeerEmpty(),
                offset_id=0,
                limit=1
            )
        )

        if hasattr(r, "count"):
            return r.count
        else:
            return len(r.messages)
