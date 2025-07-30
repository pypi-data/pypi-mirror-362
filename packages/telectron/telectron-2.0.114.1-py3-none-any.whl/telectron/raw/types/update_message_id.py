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


class UpdateMessageID(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~telectron.raw.base.Update`.

    Details:
        - Layer: ``206``
        - ID: ``4E90BFD6``

    Parameters:
        id (``int`` ``32-bit``):
            N/A

        random_id (``int`` ``64-bit``):
            N/A

    """

    __slots__: List[str] = ["id", "random_id"]

    ID = 0x4e90bfd6
    QUALNAME = "types.UpdateMessageID"

    def __init__(self, *, id: int, random_id: int) -> None:
        self.id = id  # int
        self.random_id = random_id  # long

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "UpdateMessageID":
        # No flags
        
        id = Int.read(b)
        
        random_id = Long.read(b)
        
        return UpdateMessageID(id=id, random_id=random_id)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.id))
        
        b.write(Long(self.random_id))
        
        return b.getvalue()
