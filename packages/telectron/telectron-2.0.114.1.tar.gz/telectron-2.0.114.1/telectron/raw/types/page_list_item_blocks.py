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


class PageListItemBlocks(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~telectron.raw.base.PageListItem`.

    Details:
        - Layer: ``206``
        - ID: ``25E073FC``

    Parameters:
        blocks (List of :obj:`PageBlock <telectron.raw.base.PageBlock>`):
            N/A

    """

    __slots__: List[str] = ["blocks"]

    ID = 0x25e073fc
    QUALNAME = "types.PageListItemBlocks"

    def __init__(self, *, blocks: List["raw.base.PageBlock"]) -> None:
        self.blocks = blocks  # Vector<PageBlock>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "PageListItemBlocks":
        # No flags
        
        blocks = TLObject.read(b)
        
        return PageListItemBlocks(blocks=blocks)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Vector(self.blocks))
        
        return b.getvalue()
