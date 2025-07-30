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


class FoundStickers(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~telectron.raw.base.messages.FoundStickers`.

    Details:
        - Layer: ``206``
        - ID: ``82C9E290``

    Parameters:
        hash (``int`` ``64-bit``):
            N/A

        stickers (List of :obj:`Document <telectron.raw.base.Document>`):
            N/A

        next_offset (``int`` ``32-bit``, *optional*):
            N/A

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: telectron.raw.functions

        .. autosummary::
            :nosignatures:

            messages.SearchStickers
    """

    __slots__: List[str] = ["hash", "stickers", "next_offset"]

    ID = 0x82c9e290
    QUALNAME = "types.messages.FoundStickers"

    def __init__(self, *, hash: int, stickers: List["raw.base.Document"], next_offset: Optional[int] = None) -> None:
        self.hash = hash  # long
        self.stickers = stickers  # Vector<Document>
        self.next_offset = next_offset  # flags.0?int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "FoundStickers":
        
        flags = Int.read(b)
        
        next_offset = Int.read(b) if flags & (1 << 0) else None
        hash = Long.read(b)
        
        stickers = TLObject.read(b)
        
        return FoundStickers(hash=hash, stickers=stickers, next_offset=next_offset)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.next_offset is not None else 0
        b.write(Int(flags))
        
        if self.next_offset is not None:
            b.write(Int(self.next_offset))
        
        b.write(Long(self.hash))
        
        b.write(Vector(self.stickers))
        
        return b.getvalue()
