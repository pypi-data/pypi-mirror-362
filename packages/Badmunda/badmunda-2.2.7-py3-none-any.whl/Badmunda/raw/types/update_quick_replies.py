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


class UpdateQuickReplies(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~Badmunda.raw.base.Update`.

    Details:
        - Layer: ``207``
        - ID: ``F9470AB2``

    Parameters:
        quick_replies (List of :obj:`QuickReply <Badmunda.raw.base.QuickReply>`):
            N/A

    """

    __slots__: List[str] = ["quick_replies"]

    ID = 0xf9470ab2
    QUALNAME = "types.UpdateQuickReplies"

    def __init__(self, *, quick_replies: List["raw.base.QuickReply"]) -> None:
        self.quick_replies = quick_replies  # Vector<QuickReply>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "UpdateQuickReplies":
        # No flags
        
        quick_replies = TLObject.read(b)
        
        return UpdateQuickReplies(quick_replies=quick_replies)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Vector(self.quick_replies))
        
        return b.getvalue()
