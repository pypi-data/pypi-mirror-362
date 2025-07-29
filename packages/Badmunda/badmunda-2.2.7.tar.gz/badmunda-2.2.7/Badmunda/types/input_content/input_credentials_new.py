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

from .input_credentials import InputCredentials


class InputCredentialsNew(InputCredentials):
    """Applies if a user enters new credentials on a payment provider website.

    Parameters:
        data (``str``):
            JSON-encoded data with the credential identifier from the payment provider.

        allow_save (``bool``, *optional*):
            True, if the credential identifier can be saved on the server side.
            Defaults to False.
    """
    def __init__(
        self,
        data: str,
        allow_save: bool = False,
    ):
        super().__init__()

        self.data = data
        self.allow_save = allow_save

    async def write(self, client: "Badmunda.Client"):
        return raw.types.InputPaymentCredentials(
            data=raw.types.DataJSON(data=self.data),
            save=self.allow_save
        )
