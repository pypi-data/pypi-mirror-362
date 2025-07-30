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


class MessageActionRequestedPeer(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~telectron.raw.base.MessageAction`.

    Details:
        - Layer: ``206``
        - ID: ``31518E9B``

    Parameters:
        button_id (``int`` ``32-bit``):
            N/A

        peers (List of :obj:`Peer <telectron.raw.base.Peer>`):
            N/A

    """

    __slots__: List[str] = ["button_id", "peers"]

    ID = 0x31518e9b
    QUALNAME = "types.MessageActionRequestedPeer"

    def __init__(self, *, button_id: int, peers: List["raw.base.Peer"]) -> None:
        self.button_id = button_id  # int
        self.peers = peers  # Vector<Peer>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "MessageActionRequestedPeer":
        # No flags
        
        button_id = Int.read(b)
        
        peers = TLObject.read(b)
        
        return MessageActionRequestedPeer(button_id=button_id, peers=peers)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.button_id))
        
        b.write(Vector(self.peers))
        
        return b.getvalue()
