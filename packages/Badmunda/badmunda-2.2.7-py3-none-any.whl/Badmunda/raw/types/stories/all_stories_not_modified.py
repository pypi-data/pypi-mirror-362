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


class AllStoriesNotModified(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~Badmunda.raw.base.stories.AllStories`.

    Details:
        - Layer: ``207``
        - ID: ``1158FE3E``

    Parameters:
        state (``str``):
            N/A

        stealth_mode (:obj:`StoriesStealthMode <Badmunda.raw.base.StoriesStealthMode>`):
            N/A

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: Badmunda.raw.functions

        .. autosummary::
            :nosignatures:

            stories.GetAllStories
    """

    __slots__: List[str] = ["state", "stealth_mode"]

    ID = 0x1158fe3e
    QUALNAME = "types.stories.AllStoriesNotModified"

    def __init__(self, *, state: str, stealth_mode: "raw.base.StoriesStealthMode") -> None:
        self.state = state  # string
        self.stealth_mode = stealth_mode  # StoriesStealthMode

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "AllStoriesNotModified":
        
        flags = Int.read(b)
        
        state = String.read(b)
        
        stealth_mode = TLObject.read(b)
        
        return AllStoriesNotModified(state=state, stealth_mode=stealth_mode)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        
        b.write(Int(flags))
        
        b.write(String(self.state))
        
        b.write(self.stealth_mode.write())
        
        return b.getvalue()
