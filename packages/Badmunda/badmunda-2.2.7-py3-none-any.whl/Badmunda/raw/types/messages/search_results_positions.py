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


class SearchResultsPositions(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~Badmunda.raw.base.messages.SearchResultsPositions`.

    Details:
        - Layer: ``207``
        - ID: ``53B22BAF``

    Parameters:
        count (``int`` ``32-bit``):
            N/A

        positions (List of :obj:`SearchResultsPosition <Badmunda.raw.base.SearchResultsPosition>`):
            N/A

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: Badmunda.raw.functions

        .. autosummary::
            :nosignatures:

            messages.GetSearchResultsPositions
    """

    __slots__: List[str] = ["count", "positions"]

    ID = 0x53b22baf
    QUALNAME = "types.messages.SearchResultsPositions"

    def __init__(self, *, count: int, positions: List["raw.base.SearchResultsPosition"]) -> None:
        self.count = count  # int
        self.positions = positions  # Vector<SearchResultsPosition>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "SearchResultsPositions":
        # No flags
        
        count = Int.read(b)
        
        positions = TLObject.read(b)
        
        return SearchResultsPositions(count=count, positions=positions)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.count))
        
        b.write(Vector(self.positions))
        
        return b.getvalue()
