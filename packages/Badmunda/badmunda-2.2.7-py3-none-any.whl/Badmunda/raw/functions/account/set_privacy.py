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


class SetPrivacy(TLObject):  # type: ignore
    """Telegram API function.

    Details:
        - Layer: ``207``
        - ID: ``C9F81CE8``

    Parameters:
        key (:obj:`InputPrivacyKey <Badmunda.raw.base.InputPrivacyKey>`):
            N/A

        rules (List of :obj:`InputPrivacyRule <Badmunda.raw.base.InputPrivacyRule>`):
            N/A

    Returns:
        :obj:`account.PrivacyRules <Badmunda.raw.base.account.PrivacyRules>`
    """

    __slots__: List[str] = ["key", "rules"]

    ID = 0xc9f81ce8
    QUALNAME = "functions.account.SetPrivacy"

    def __init__(self, *, key: "raw.base.InputPrivacyKey", rules: List["raw.base.InputPrivacyRule"]) -> None:
        self.key = key  # InputPrivacyKey
        self.rules = rules  # Vector<InputPrivacyRule>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "SetPrivacy":
        # No flags
        
        key = TLObject.read(b)
        
        rules = TLObject.read(b)
        
        return SetPrivacy(key=key, rules=rules)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.key.write())
        
        b.write(Vector(self.rules))
        
        return b.getvalue()
