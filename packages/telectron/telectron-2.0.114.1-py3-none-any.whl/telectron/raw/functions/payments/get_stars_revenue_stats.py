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


class GetStarsRevenueStats(TLObject):  # type: ignore
    """Telegram API function.

    Details:
        - Layer: ``206``
        - ID: ``D91FFAD6``

    Parameters:
        peer (:obj:`InputPeer <telectron.raw.base.InputPeer>`):
            N/A

        dark (``bool``, *optional*):
            N/A

        ton (``bool``, *optional*):
            N/A

    Returns:
        :obj:`payments.StarsRevenueStats <telectron.raw.base.payments.StarsRevenueStats>`
    """

    __slots__: List[str] = ["peer", "dark", "ton"]

    ID = 0xd91ffad6
    QUALNAME = "functions.payments.GetStarsRevenueStats"

    def __init__(self, *, peer: "raw.base.InputPeer", dark: Optional[bool] = None, ton: Optional[bool] = None) -> None:
        self.peer = peer  # InputPeer
        self.dark = dark  # flags.0?true
        self.ton = ton  # flags.1?true

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "GetStarsRevenueStats":
        
        flags = Int.read(b)
        
        dark = True if flags & (1 << 0) else False
        ton = True if flags & (1 << 1) else False
        peer = TLObject.read(b)
        
        return GetStarsRevenueStats(peer=peer, dark=dark, ton=ton)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.dark else 0
        flags |= (1 << 1) if self.ton else 0
        b.write(Int(flags))
        
        b.write(self.peer.write())
        
        return b.getvalue()
