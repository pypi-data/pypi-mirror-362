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

from typing import Dict, List, Optional

import Badmunda
from Badmunda import raw, types

from ..object import Object


class MessageReactions(Object):
    """Contains information about a message reactions.

    Parameters:
        reactions (List of :obj:`~Badmunda.types.Reaction`):
            Reactions list.

        are_tags (``bool``, *optional*):
            True, if the reactions are tags and Telegram Premium users can filter messages by them.

        paid_reactors (List of :obj:`~Badmunda.types.PaidReactor`, *optional*):
            Information about top users that added the paid reaction.

        can_get_added_reactions (``bool``, *optional*):
            True, if the list of added reactions is available using :meth:`~Badmunda.Client.get_message_added_reactions`.
    """

    # TODO: Add get_message_added_reactions method

    def __init__(
        self,
        *,
        client: "Badmunda.Client" = None,
        reactions: Optional[List["types.Reaction"]] = None,
        are_tags: Optional[bool] = None,
        paid_reactors: Optional[List["types.PaidReactor"]] = None,
        can_get_added_reactions: Optional[bool] = None,
    ):
        super().__init__(client)

        self.reactions = reactions
        self.are_tags = are_tags
        self.paid_reactors = paid_reactors
        self.can_get_added_reactions = can_get_added_reactions

    @staticmethod
    def _parse(
        client: "Badmunda.Client",
        message_reactions: Optional["raw.base.MessageReactions"],
        users: Dict[int, "types.User"],
        chats: Dict[int, "types.Chat"],
    ) -> Optional["MessageReactions"]:
        if not message_reactions:
            return None

        return MessageReactions(
            client=client,
            reactions=types.List(
                [
                    types.Reaction._parse_count(client, reaction)
                    for reaction in message_reactions.results
                ]
            ),
            are_tags=message_reactions.reactions_as_tags,
            paid_reactors=types.List(
                [
                    types.PaidReactor._parse(client, paid_reactor, users, chats)
                    for paid_reactor in message_reactions.top_reactors
                ]
            )
            if message_reactions.top_reactors
            else None,
            can_get_added_reactions=message_reactions.can_see_list,
        )
