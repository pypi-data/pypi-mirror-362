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


class GetSavedDialogsByID(TLObject):  # type: ignore
    """Telegram API function.

    Details:
        - Layer: ``207``
        - ID: ``6F6F9C96``

    Parameters:
        ids (List of :obj:`InputPeer <Badmunda.raw.base.InputPeer>`):
            N/A

        parent_peer (:obj:`InputPeer <Badmunda.raw.base.InputPeer>`, *optional*):
            N/A

    Returns:
        :obj:`messages.SavedDialogs <Badmunda.raw.base.messages.SavedDialogs>`
    """

    __slots__: List[str] = ["ids", "parent_peer"]

    ID = 0x6f6f9c96
    QUALNAME = "functions.messages.GetSavedDialogsByID"

    def __init__(self, *, ids: List["raw.base.InputPeer"], parent_peer: "raw.base.InputPeer" = None) -> None:
        self.ids = ids  # Vector<InputPeer>
        self.parent_peer = parent_peer  # flags.1?InputPeer

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "GetSavedDialogsByID":
        
        flags = Int.read(b)
        
        parent_peer = TLObject.read(b) if flags & (1 << 1) else None
        
        ids = TLObject.read(b)
        
        return GetSavedDialogsByID(ids=ids, parent_peer=parent_peer)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 1) if self.parent_peer is not None else 0
        b.write(Int(flags))
        
        if self.parent_peer is not None:
            b.write(self.parent_peer.write())
        
        b.write(Vector(self.ids))
        
        return b.getvalue()
