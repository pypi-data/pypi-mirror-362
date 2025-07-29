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

from uuid import uuid4

import Badmunda
from Badmunda import types
from ..object import Object


class InlineQueryResult(Object):
    """One result of an inline query.

    - :obj:`~Badmunda.types.InlineQueryResultCachedAudio`
    - :obj:`~Badmunda.types.InlineQueryResultCachedDocument`
    - :obj:`~Badmunda.types.InlineQueryResultCachedAnimation`
    - :obj:`~Badmunda.types.InlineQueryResultCachedPhoto`
    - :obj:`~Badmunda.types.InlineQueryResultCachedSticker`
    - :obj:`~Badmunda.types.InlineQueryResultCachedVideo`
    - :obj:`~Badmunda.types.InlineQueryResultCachedVoice`
    - :obj:`~Badmunda.types.InlineQueryResultArticle`
    - :obj:`~Badmunda.types.InlineQueryResultAudio`
    - :obj:`~Badmunda.types.InlineQueryResultContact`
    - :obj:`~Badmunda.types.InlineQueryResultDocument`
    - :obj:`~Badmunda.types.InlineQueryResultAnimation`
    - :obj:`~Badmunda.types.InlineQueryResultLocation`
    - :obj:`~Badmunda.types.InlineQueryResultPhoto`
    - :obj:`~Badmunda.types.InlineQueryResultVenue`
    - :obj:`~Badmunda.types.InlineQueryResultVideo`
    - :obj:`~Badmunda.types.InlineQueryResultVoice`
    """

    def __init__(
        self,
        type: str,
        id: str,
        input_message_content: "types.InputMessageContent",
        reply_markup: "types.InlineKeyboardMarkup"
    ):
        super().__init__()

        self.type = type
        self.id = str(uuid4()) if id is None else str(id)
        self.input_message_content = input_message_content
        self.reply_markup = reply_markup

    async def write(self, client: "Badmunda.Client"):
        pass
