#  telectron - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of telectron.
#
#  telectron is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  telectron is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with telectron.  If not, see <http://www.gnu.org/licenses/>.

from io import BytesIO

from telectron.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from telectron.raw.core import TLObject
from telectron import raw
from typing import List, Optional, Any

# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #


class MessageMediaPoll(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~telectron.raw.base.MessageMedia`.

    Details:
        - Layer: ``206``
        - ID: ``4BD6E798``

    Parameters:
        poll (:obj:`Poll <telectron.raw.base.Poll>`):
            N/A

        results (:obj:`PollResults <telectron.raw.base.PollResults>`):
            N/A

    Functions:
        This object can be returned by 2 functions.

        .. currentmodule:: telectron.raw.functions

        .. autosummary::
            :nosignatures:

            messages.UploadMedia
            messages.UploadImportedMedia
    """

    __slots__: List[str] = ["poll", "results"]

    ID = 0x4bd6e798
    QUALNAME = "types.MessageMediaPoll"

    def __init__(self, *, poll: "raw.base.Poll", results: "raw.base.PollResults") -> None:
        self.poll = poll  # Poll
        self.results = results  # PollResults

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "MessageMediaPoll":
        # No flags
        
        poll = TLObject.read(b)
        
        results = TLObject.read(b)
        
        return MessageMediaPoll(poll=poll, results=results)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.poll.write())
        
        b.write(self.results.write())
        
        return b.getvalue()
