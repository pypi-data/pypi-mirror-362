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
from ..object import Object


class BotCommandScope(Object):
    """Represents the scope to which bot commands are applied.

    Currently, the following 7 scopes are supported:

    - :obj:`~Badmunda.types.BotCommandScopeDefault`
    - :obj:`~Badmunda.types.BotCommandScopeAllPrivateChats`
    - :obj:`~Badmunda.types.BotCommandScopeAllGroupChats`
    - :obj:`~Badmunda.types.BotCommandScopeAllChatAdministrators`
    - :obj:`~Badmunda.types.BotCommandScopeChat`
    - :obj:`~Badmunda.types.BotCommandScopeChatAdministrators`
    - :obj:`~Badmunda.types.BotCommandScopeChatMember`

    **Determining list of commands**

    The following algorithm is used to determine the list of commands for a particular user viewing the bot menu.
    The first list of commands which is set is returned:

    **Commands in the chat with the bot**:

    - BotCommandScopeChat + language_code
    - BotCommandScopeChat
    - BotCommandScopeAllPrivateChats + language_code
    - BotCommandScopeAllPrivateChats
    - BotCommandScopeDefault + language_code
    - BotCommandScopeDefault

    **Commands in group and supergroup chats**

    - BotCommandScopeChatMember + language_code
    - BotCommandScopeChatMember
    - BotCommandScopeChatAdministrators + language_code (administrators only)
    - BotCommandScopeChatAdministrators (administrators only)
    - BotCommandScopeChat + language_code
    - BotCommandScopeChat
    - BotCommandScopeAllChatAdministrators + language_code (administrators only)
    - BotCommandScopeAllChatAdministrators (administrators only)
    - BotCommandScopeAllGroupChats + language_code
    - BotCommandScopeAllGroupChats
    - BotCommandScopeDefault + language_code
    - BotCommandScopeDefault
    """

    def __init__(self, type: str):
        super().__init__()

        self.type = type

    async def write(self, client: "Badmunda.Client") -> "raw.base.BotCommandScope":
        raise NotImplementedError
