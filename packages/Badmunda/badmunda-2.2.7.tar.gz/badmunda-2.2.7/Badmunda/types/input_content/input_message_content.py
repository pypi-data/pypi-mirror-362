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

from ..object import Object


class InputMessageContent(Object):
    """Content of a message to be sent as a result of an inline query.

    Badmunda currently supports the following types:

    - :obj:`~Badmunda.types.InputTextMessageContent`
    - :obj:`~Badmunda.types.InputLocationMessageContent`
    - :obj:`~Badmunda.types.InputVenueMessageContent`
    - :obj:`~Badmunda.types.InputContactMessageContent`
    - :obj:`~Badmunda.types.InputInvoiceMessageContent`
    """

    def __init__(self):
        super().__init__()

    async def write(self, client: "Badmunda.Client", reply_markup):
        raise NotImplementedError
