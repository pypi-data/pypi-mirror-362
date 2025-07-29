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

from typing import Dict

import Badmunda
from Badmunda import raw, utils
from Badmunda import types
from ..object import Object
from ..update import Update


class ChatBoostUpdated(Object, Update):
    """A channel/supergroup boost has changed (bots only).

    Parameters:
        chat (:obj:`~Badmunda.types.Chat`):
            The chat where boost was changed.

        boost (:obj:`~Badmunda.types.ChatBoost`):
            New boost information.
    """

    def __init__(
        self,
        *,
        client: "Badmunda.Client" = None,
        chat: "types.Chat",
        boost: "types.ChatBoost"
    ):
        super().__init__(client)

        self.chat = chat
        self.boost = boost

    @staticmethod
    def _parse(
        client: "Badmunda.Client",
        update: "raw.types.UpdateBotChatBoost",
        users: Dict[int, "raw.types.User"],
        chats: Dict[int, "raw.types.Channel"],
    ) -> "ChatBoostUpdated":
        return ChatBoostUpdated(
            chat=types.Chat._parse_channel_chat(client, chats.get(utils.get_raw_peer_id(update.peer))),
            boost=types.ChatBoost._parse(client, update.boost, users),
            client=client
        )
