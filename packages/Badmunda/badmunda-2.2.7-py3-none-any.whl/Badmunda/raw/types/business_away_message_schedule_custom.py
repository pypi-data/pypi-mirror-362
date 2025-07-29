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

from io import BytesIO

<<<<<<< HEAD
from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
=======
from Badmunda.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from Badmunda.raw.core import TLObject
from Badmunda import raw
>>>>>>> f7f5e654 (?? Clean history and fixed broken tree)
from typing import List, Optional, Any

# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #


class BusinessAwayMessageScheduleCustom(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~Badmunda.raw.base.BusinessAwayMessageSchedule`.

    Details:
        - Layer: ``207``
        - ID: ``CC4D9ECC``

    Parameters:
        start_date (``int`` ``32-bit``):
            N/A

        end_date (``int`` ``32-bit``):
            N/A

    """

    __slots__: List[str] = ["start_date", "end_date"]

    ID = 0xcc4d9ecc
    QUALNAME = "types.BusinessAwayMessageScheduleCustom"

    def __init__(self, *, start_date: int, end_date: int) -> None:
        self.start_date = start_date  # int
        self.end_date = end_date  # int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "BusinessAwayMessageScheduleCustom":
        # No flags
        
        start_date = Int.read(b)
        
        end_date = Int.read(b)
        
        return BusinessAwayMessageScheduleCustom(start_date=start_date, end_date=end_date)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.start_date))
        
        b.write(Int(self.end_date))
        
        return b.getvalue()
