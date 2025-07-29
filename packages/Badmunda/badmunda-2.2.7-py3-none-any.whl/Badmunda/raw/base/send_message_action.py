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
SendMessageAction = Union[raw.types.SendMessageCancelAction, raw.types.SendMessageChooseContactAction, raw.types.SendMessageChooseStickerAction, raw.types.SendMessageEmojiInteraction, raw.types.SendMessageEmojiInteractionSeen, raw.types.SendMessageGamePlayAction, raw.types.SendMessageGeoLocationAction, raw.types.SendMessageHistoryImportAction, raw.types.SendMessageRecordAudioAction, raw.types.SendMessageRecordRoundAction, raw.types.SendMessageRecordVideoAction, raw.types.SendMessageTypingAction, raw.types.SendMessageUploadAudioAction, raw.types.SendMessageUploadDocumentAction, raw.types.SendMessageUploadPhotoAction, raw.types.SendMessageUploadRoundAction, raw.types.SendMessageUploadVideoAction, raw.types.SpeakingInGroupCallAction]
SendMessageAction.__doc__ = """
    Telegram API base type.

    Constructors:
        This base type has 18 constructors available.

        .. currentmodule:: Badmunda.raw.types

        .. autosummary::
            :nosignatures:

            SendMessageCancelAction
            SendMessageChooseContactAction
            SendMessageChooseStickerAction
            SendMessageEmojiInteraction
            SendMessageEmojiInteractionSeen
            SendMessageGamePlayAction
            SendMessageGeoLocationAction
            SendMessageHistoryImportAction
            SendMessageRecordAudioAction
            SendMessageRecordRoundAction
            SendMessageRecordVideoAction
            SendMessageTypingAction
            SendMessageUploadAudioAction
            SendMessageUploadDocumentAction
            SendMessageUploadPhotoAction
            SendMessageUploadRoundAction
            SendMessageUploadVideoAction
            SpeakingInGroupCallAction
"""
