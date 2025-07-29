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

import logging
from typing import Optional

import Badmunda
from Badmunda import raw

from .input_message_content import InputMessageContent

log = logging.getLogger(__name__)


class InputContactMessageContent(InputMessageContent):
    """Content of a contact message to be sent as the result of an inline query.

    Parameters:
        phone_number (``str``):
            Contact's phone number.

        first_name (``str``):
            Contact's first name.

        last_name (``str``, *optional*):
            Contact's last name.

        vcard (``str``, *optional*):
            Additional data about the contact in the form of a `vCard <https://en.wikipedia.org/wiki/VCard>`_, 0-2048 bytes.
    """

    def __init__(
        self,
        phone_number: str,
        first_name: str,
        last_name: Optional[str] = None,
        vcard: Optional[str] = None
    ):
        super().__init__()

        self.phone_number = phone_number
        self.first_name = first_name
        self.last_name = last_name
        self.vcard = vcard

    async def write(self, client: "Badmunda.Client", reply_markup):
        return raw.types.InputBotInlineMessageMediaContact(
            phone_number=self.phone_number,
            first_name=self.first_name,
            last_name=self.last_name,
            vcard=self.vcard,
            reply_markup=await reply_markup.write(client) if reply_markup else None
        )
