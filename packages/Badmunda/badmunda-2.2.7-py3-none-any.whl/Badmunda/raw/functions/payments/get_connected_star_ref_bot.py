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


class GetConnectedStarRefBot(TLObject):  # type: ignore
    """Telegram API function.

    Details:
        - Layer: ``207``
        - ID: ``B7D998F0``

    Parameters:
        peer (:obj:`InputPeer <Badmunda.raw.base.InputPeer>`):
            N/A

        bot (:obj:`InputUser <Badmunda.raw.base.InputUser>`):
            N/A

    Returns:
        :obj:`payments.ConnectedStarRefBots <Badmunda.raw.base.payments.ConnectedStarRefBots>`
    """

    __slots__: List[str] = ["peer", "bot"]

    ID = 0xb7d998f0
    QUALNAME = "functions.payments.GetConnectedStarRefBot"

    def __init__(self, *, peer: "raw.base.InputPeer", bot: "raw.base.InputUser") -> None:
        self.peer = peer  # InputPeer
        self.bot = bot  # InputUser

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "GetConnectedStarRefBot":
        # No flags
        
        peer = TLObject.read(b)
        
        bot = TLObject.read(b)
        
        return GetConnectedStarRefBot(peer=peer, bot=bot)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.peer.write())
        
        b.write(self.bot.write())
        
        return b.getvalue()
