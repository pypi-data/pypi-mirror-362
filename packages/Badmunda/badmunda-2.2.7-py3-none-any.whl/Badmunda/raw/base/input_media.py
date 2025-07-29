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
InputMedia = Union[raw.types.InputMediaContact, raw.types.InputMediaDice, raw.types.InputMediaDocument, raw.types.InputMediaDocumentExternal, raw.types.InputMediaEmpty, raw.types.InputMediaGame, raw.types.InputMediaGeoLive, raw.types.InputMediaGeoPoint, raw.types.InputMediaInvoice, raw.types.InputMediaPaidMedia, raw.types.InputMediaPhoto, raw.types.InputMediaPhotoExternal, raw.types.InputMediaPoll, raw.types.InputMediaStory, raw.types.InputMediaTodo, raw.types.InputMediaUploadedDocument, raw.types.InputMediaUploadedPhoto, raw.types.InputMediaVenue, raw.types.InputMediaWebPage]
InputMedia.__doc__ = """
    Telegram API base type.

    Constructors:
        This base type has 19 constructors available.

        .. currentmodule:: Badmunda.raw.types

        .. autosummary::
            :nosignatures:

            InputMediaContact
            InputMediaDice
            InputMediaDocument
            InputMediaDocumentExternal
            InputMediaEmpty
            InputMediaGame
            InputMediaGeoLive
            InputMediaGeoPoint
            InputMediaInvoice
            InputMediaPaidMedia
            InputMediaPhoto
            InputMediaPhotoExternal
            InputMediaPoll
            InputMediaStory
            InputMediaTodo
            InputMediaUploadedDocument
            InputMediaUploadedPhoto
            InputMediaVenue
            InputMediaWebPage
"""
