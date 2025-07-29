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

# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #

from typing import Union
<<<<<<< HEAD
from pyrogram import raw
from pyrogram.raw.core import TLObject
=======
from Badmunda import raw
from Badmunda.raw.core import TLObject
>>>>>>> f7f5e654 (?? Clean history and fixed broken tree)

# We need to dynamically set `__doc__` due to `sphinx`
InputPrivacyKey = Union[raw.types.InputPrivacyKeyAbout, raw.types.InputPrivacyKeyAddedByPhone, raw.types.InputPrivacyKeyBirthday, raw.types.InputPrivacyKeyChatInvite, raw.types.InputPrivacyKeyForwards, raw.types.InputPrivacyKeyNoPaidMessages, raw.types.InputPrivacyKeyPhoneCall, raw.types.InputPrivacyKeyPhoneNumber, raw.types.InputPrivacyKeyPhoneP2P, raw.types.InputPrivacyKeyProfilePhoto, raw.types.InputPrivacyKeyStarGiftsAutoSave, raw.types.InputPrivacyKeyStatusTimestamp, raw.types.InputPrivacyKeyVoiceMessages]
InputPrivacyKey.__doc__ = """
    Telegram API base type.

    Constructors:
        This base type has 13 constructors available.

        .. currentmodule:: Badmunda.raw.types

        .. autosummary::
            :nosignatures:

            InputPrivacyKeyAbout
            InputPrivacyKeyAddedByPhone
            InputPrivacyKeyBirthday
            InputPrivacyKeyChatInvite
            InputPrivacyKeyForwards
            InputPrivacyKeyNoPaidMessages
            InputPrivacyKeyPhoneCall
            InputPrivacyKeyPhoneNumber
            InputPrivacyKeyPhoneP2P
            InputPrivacyKeyProfilePhoto
            InputPrivacyKeyStarGiftsAutoSave
            InputPrivacyKeyStatusTimestamp
            InputPrivacyKeyVoiceMessages
"""
