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


class GetCustomEmojiDocuments(TLObject):  # type: ignore
    """Telegram API function.

    Details:
        - Layer: ``206``
        - ID: ``D9AB0F54``

    Parameters:
        document_id (List of ``int`` ``64-bit``):
            N/A

    Returns:
        List of :obj:`Document <telectron.raw.base.Document>`
    """

    __slots__: List[str] = ["document_id"]

    ID = 0xd9ab0f54
    QUALNAME = "functions.messages.GetCustomEmojiDocuments"

    def __init__(self, *, document_id: List[int]) -> None:
        self.document_id = document_id  # Vector<long>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "GetCustomEmojiDocuments":
        # No flags
        
        document_id = TLObject.read(b, Long)
        
        return GetCustomEmojiDocuments(document_id=document_id)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Vector(self.document_id, Long))
        
        return b.getvalue()
