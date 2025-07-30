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


class JoinChatlistInvite(TLObject):  # type: ignore
    """Telegram API function.

    Details:
        - Layer: ``206``
        - ID: ``A6B1E39A``

    Parameters:
        slug (``str``):
            N/A

        peers (List of :obj:`InputPeer <telectron.raw.base.InputPeer>`):
            N/A

    Returns:
        :obj:`Updates <telectron.raw.base.Updates>`
    """

    __slots__: List[str] = ["slug", "peers"]

    ID = 0xa6b1e39a
    QUALNAME = "functions.chatlists.JoinChatlistInvite"

    def __init__(self, *, slug: str, peers: List["raw.base.InputPeer"]) -> None:
        self.slug = slug  # string
        self.peers = peers  # Vector<InputPeer>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "JoinChatlistInvite":
        # No flags
        
        slug = String.read(b)
        
        peers = TLObject.read(b)
        
        return JoinChatlistInvite(slug=slug, peers=peers)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.slug))
        
        b.write(Vector(self.peers))
        
        return b.getvalue()
