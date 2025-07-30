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


class TogglePeerStoriesHidden(TLObject):  # type: ignore
    """Telegram API function.

    Details:
        - Layer: ``206``
        - ID: ``BD0415C4``

    Parameters:
        peer (:obj:`InputPeer <telectron.raw.base.InputPeer>`):
            N/A

        hidden (``bool``):
            N/A

    Returns:
        ``bool``
    """

    __slots__: List[str] = ["peer", "hidden"]

    ID = 0xbd0415c4
    QUALNAME = "functions.stories.TogglePeerStoriesHidden"

    def __init__(self, *, peer: "raw.base.InputPeer", hidden: bool) -> None:
        self.peer = peer  # InputPeer
        self.hidden = hidden  # Bool

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "TogglePeerStoriesHidden":
        # No flags
        
        peer = TLObject.read(b)
        
        hidden = Bool.read(b)
        
        return TogglePeerStoriesHidden(peer=peer, hidden=hidden)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.peer.write())
        
        b.write(Bool(self.hidden))
        
        return b.getvalue()
